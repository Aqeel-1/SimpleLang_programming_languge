# --- AST Node Classes ---
class Program:
    def __init__(self, declarations):
        self.declarations = declarations  # list of top-level declarations

    def __repr__(self):
        return f"Program(declarations={self.declarations})"

class FunctionDeclaration:
    def __init__(self, return_type, name, parameters, body):
        self.return_type = return_type
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        return (f"FunctionDeclaration(return_type={self.return_type}, name={self.name}, "
                f"params={self.parameters}, body={self.body})")

class Parameter:
    def __init__(self, param_type, name):
        self.param_type = param_type
        self.name = name

    def __repr__(self):
        return f"Parameter(type={self.param_type}, name={self.name})"

class BlockStatement:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f"BlockStatement(statements={self.statements})"

class VariableDeclaration:
    def __init__(self, var_type, name, initializer):
        self.var_type = var_type
        self.name = name
        self.initializer = initializer

    def __repr__(self):
        return (f"VariableDeclaration(type={self.var_type}, name={self.name}, "
                f"initializer={self.initializer})")

class ReturnStatement:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"ReturnStatement(expression={self.expression})"

class IfStatement:
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def __repr__(self):
        return (f"IfStatement(cond={self.condition}, then={self.then_branch}, "
                f"else={self.else_branch})")

class WhileStatement:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"WhileStatement(condition={self.condition}, body={self.body})"

class ForStatement:
    def __init__(self, init, condition, increment, body):
        self.init = init
        self.condition = condition
        self.increment = increment
        self.body = body

    def __repr__(self):
        return (f"ForStatement(init={self.init}, condition={self.condition}, "
                f"increment={self.increment}, body={self.body})")

class ExpressionStatement:
    def __init__(self, expression):
        self.expression = expression

    def __repr__(self):
        return f"ExpressionStatement(expression={self.expression})"

# --- Expression Nodes ---
class BinaryExpression:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return (f"BinaryExpression(left={self.left}, op={self.operator}, "
                f"right={self.right})")

class FunctionCall:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def __repr__(self):
        return f"FunctionCall(name={self.name}, args={self.arguments})"

class Identifier:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Identifier(name={self.name})"

class NumberLiteral:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumberLiteral(value={self.value})"

class StringLiteral:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"StringLiteral(value={self.value})"
