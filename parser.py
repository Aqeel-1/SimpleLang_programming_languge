from ast_def import *


class SimpleLangParserError(Exception):
    """Custom exception for parser errors."""
    pass


# --- Parser ---
class SimpleLangParser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.length = len(tokens)

    def _peek(self, offset=0):
        pos = self.position + offset
        if pos < self.length:
            return self.tokens[pos]
        return None

    def _advance(self):
        """Consume and return the current token."""
        token = self._peek()
        self.position += 1
        return token

    def _match(self, *token_values):
        """
        If the current token's value is among token_values, consume it and return True.
        Otherwise, return False.
        """
        current = self._peek()
        if current and current.value in token_values:
            self._advance()
            return True
        return False

    def _match_type(self, *token_types):
        """
        If the current token's type is among token_types, consume it and return that token.
        Otherwise, return None.
        """
        current = self._peek()
        if current and current.type in token_types:
            return self._advance()
        return None

    def _expect_value(self, value):
        """
        Expect the current token to have a specific `value`; otherwise raise an error.
        """
        token = self._peek()
        if not token or token.value != value:
            raise SimpleLangParserError(
                f"Expected token value '{value}' but got '{token.value if token else None}'."
            )
        return self._advance()

    def _expect_type(self, token_type):
        """
        Expect the current token to have type `token_type`; otherwise raise an error.
        """
        token = self._peek()
        if not token or token.type != token_type:
            raise SimpleLangParserError(
                f"Expected token type '{token_type}' but got '{token.type if token else None}'."
            )
        return self._advance()

    def parse(self):
        declarations = []
        while self._peek():
            declarations.append(self.parse_declaration())
        return Program(declarations)

    def parse_declaration(self):
        """
        A top-level declaration can be:
        - A function declaration
        - A variable declaration
        """
        type_token = self._expect_type("KEYWORD")
        name_token = self._expect_type("IDENTIFIER")
        if self._peek() and self._peek().value == "(":
            return self.parse_function_declaration(type_token.value, name_token.value)
        else:
            return self.parse_global_variable_declaration(type_token.value, name_token.value)

    def parse_function_declaration(self, return_type, func_name):
        self._expect_value("(")
        parameters = []
        if self._peek() and self._peek().value != ")":
            parameters = self.parse_parameter_list()
        self._expect_value(")")
        body = self.parse_block_statement()
        return FunctionDeclaration(return_type, func_name, parameters, body)

    def parse_parameter_list(self):
        params = []
        while True:
            param_type_token = self._expect_type("KEYWORD")
            param_name_token = self._expect_type("IDENTIFIER")
            params.append(Parameter(param_type_token.value, param_name_token.value))
            if not self._match(","):
                break
        return params

    def parse_block_statement(self):
        self._expect_value("{")
        statements = []
        while self._peek() and self._peek().value != "}":
            statements.append(self.parse_statement())
        self._expect_value("}")
        return BlockStatement(statements)

    def parse_global_variable_declaration(self, var_type, var_name):
        initializer = None
        if self._match("="):
            initializer = self.parse_expression()
        self._expect_value(";")
        return VariableDeclaration(var_type, var_name, initializer)

    def parse_statement(self):
        token = self._peek()
        if token.type == "KEYWORD" and token.value in ("whole", "fraction", "letter", "text"):
            return self.parse_variable_declaration()
        if token.type == "KEYWORD" and token.value == "output":
            return self.parse_return_statement()
        if token.type == "KEYWORD" and token.value == "check":
            return self.parse_if_statement()
        if token.type == "KEYWORD" and token.value == "loop":
            return self.parse_while_statement()
        if token.type == "KEYWORD" and token.value == "iterate":
            return self.parse_for_statement()
        if token.value == "{":
            return self.parse_block_statement()
        return self.parse_expression_statement()

    def parse_variable_declaration(self):
        var_type_token = self._advance()
        name_token = self._expect_type("IDENTIFIER")
        initializer = None
        if self._match("="):
            initializer = self.parse_expression()
        self._expect_value(";")
        return VariableDeclaration(var_type_token.value, name_token.value, initializer)

    def parse_return_statement(self):
        self._advance()
        expr = None
        if self._peek() and self._peek().value != ";":
            expr = self.parse_expression()
        self._expect_value(";")
        return ReturnStatement(expr)

    def parse_if_statement(self):
        self._advance()
        self._expect_value("(")
        condition = self.parse_expression()
        self._expect_value(")")
        then_branch = self.parse_statement()
        else_branch = None
        if self._peek() and self._peek().value == "otherwise":
            self._advance()
            else_branch = self.parse_statement()
        return IfStatement(condition, then_branch, else_branch)

    def parse_while_statement(self):
        self._advance()
        self._expect_value("(")
        condition = self.parse_expression()
        self._expect_value(")")
        body = self.parse_statement()
        return WhileStatement(condition, body)

    def parse_for_statement(self):
        self._advance()
        self._expect_value("(")
        init = None
        if self._peek() and self._peek().value != ";":
            init = self.parse_expression()
        self._expect_value(";")
        condition = None
        if self._peek() and self._peek().value != ";":
            condition = self.parse_expression()
        self._expect_value(";")
        increment = None
        if self._peek() and self._peek().value != ")":
            increment = self.parse_expression()
        self._expect_value(")")
        body = self.parse_statement()
        return ForStatement(init, condition, increment, body)

    def parse_expression_statement(self):
        expr = self.parse_expression()
        self._expect_value(";")
        return ExpressionStatement(expr)

    def parse_expression(self):
        return self.parse_comparison_expression()

    def parse_comparison_expression(self):
        expr = self.parse_additive_expression()
        while True:
            token = self._peek()
            if token and token.value in {"==", "!=", "<", ">", "<=", ">="}:
                op = self._advance().value
                right = self.parse_additive_expression()
                expr = BinaryExpression(expr, op, right)
            else:
                break
        return expr

    def parse_additive_expression(self):
        expr = self.parse_primary()
        while True:
            token = self._peek()
            if token and token.value in {"+", "-"}:
                op = self._advance().value
                right = self.parse_primary()
                expr = BinaryExpression(expr, op, right)
            else:
                break
        return expr

    def parse_primary(self):
        token = self._peek()
        if token.type == "NUMBER":
            self._advance()
            return NumberLiteral(token.value)
        if token.type == "STRING_LITERAL":
            self._advance()
            return StringLiteral(token.value)
        if token.type == "IDENTIFIER":
            ident = token.value
            self._advance()
            if self._peek() and self._peek().value == "(":
                return self.parse_function_call(ident)
            return Identifier(ident)
        if token.value == "(":
            self._advance()
            expr = self.parse_expression()
            self._expect_value(")")
            return expr
        raise SimpleLangParserError(f"Unexpected token: {token}")

    def parse_function_call(self, func_name):
        self._expect_value("(")
        args = []
        if self._peek() and self._peek().value != ")":
            while True:
                args.append(self.parse_expression())
                if not self._match(","):
                    break
        self._expect_value(")")
        return FunctionCall(func_name, args)