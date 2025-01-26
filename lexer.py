from token_def import Token


class SimpleLangLexerError(Exception):
    """Custom exception class for lexer errors."""
    pass


class SimpleLangLexer:
    # Reserved words in SimpleLang
    RESERVED_WORDS = {
        "whole", "fraction", "letter", "text", "check", "otherwise",
        "loop", "iterate", "output"
    }

    # Operators and punctuation
    OPERATORS = {
        "+", "-", "*", "/", "%", "==", "!=", "<", ">", "<=", ">=", "=",
        "++", "--", "+=", "-=", "*=", "/=",
        # You could add more C-like operators here as needed
    }
    PUNCTUATION = {
        "(", ")", "{", "}", ",", ";"
        # Add more if needed
    }

    def __init__(self, source_code):
        self.source = source_code
        self.position = 0
        self.line = 1
        self.column = 1
        self.length = len(source_code)

    def _peek(self, offset=0):
        """Look at the character at current position + offset without consuming it."""
        pos = self.position + offset
        if pos < self.length:
            return self.source[pos]
        return None

    def _advance(self):
        """Consume one character and move forward."""
        ch = self._peek()
        if ch == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        self.position += 1
        return ch

    def _match(self, text):
        """Attempt to match the string `text` at the current position."""
        end_pos = self.position + len(text)
        if self.source[self.position:end_pos] == text:
            # Advance
            for _ in range(len(text)):
                self._advance()
            return True
        return False

    def _skip_whitespace(self):
        """Skip spaces, tabs, and newlines (but track line/column)."""
        while True:
            ch = self._peek()
            if ch is not None and ch.isspace():
                self._advance()
            else:
                break

    def _read_number(self):
        """Read a numeric literal (integer or float)."""
        start_line, start_col = self.line, self.column
        num_str = ""
        has_decimal_point = False

        while True:
            ch = self._peek()
            if ch is None or not (ch.isdigit() or ch == "."):
                break
            if ch == ".":
                if has_decimal_point:
                    # second decimal point => break
                    break
                has_decimal_point = True
            num_str += self._advance()
        return Token("NUMBER", num_str, start_line, start_col)

    def _read_identifier_or_keyword(self):
        """Read an identifier; could also be a keyword."""
        start_line, start_col = self.line, self.column
        ident = ""
        while True:
            ch = self._peek()
            if ch is None or not (ch.isalnum() or ch == "_"):
                break
            ident += self._advance()
        if ident in self.RESERVED_WORDS:
            return Token("KEYWORD", ident, start_line, start_col)
        return Token("IDENTIFIER", ident, start_line, start_col)

    def _read_string_literal(self):
        """Read a string literal enclosed in double quotes, supporting basic escapes."""
        start_line, start_col = self.line, self.column
        # Consume the opening quote
        self._advance()
        string_val = ""
        while True:
            ch = self._peek()
            if ch is None:
                raise SimpleLangLexerError(f"Unterminated string at line {start_line}, col {start_col}")
            if ch == '"':
                # Closing quote
                self._advance()
                break
            if ch == "\\":
                # Handle escapes
                self._advance()
                escaped_char = self._peek()
                if escaped_char in ['"', '\\', 'n']:
                    if escaped_char == 'n':
                        string_val += "\n"
                    else:
                        string_val += escaped_char
                    self._advance()
                else:
                    # Unrecognized escape - just take the char as-is
                    if escaped_char is not None:
                        string_val += escaped_char
                        self._advance()
            else:
                string_val += self._advance()
        return Token("STRING_LITERAL", string_val, start_line, start_col)

    def _read_comment(self):
        """Read either a single-line or multi-line comment."""
        start_line, start_col = self.line, self.column

        # We already know the initial sentinel is found
        if self._match("!!"):
            # single-line comment
            # read until newline or end
            comment_text = ""
            while True:
                ch = self._peek()
                if ch is None or ch == "\n":
                    break
                comment_text += self._advance()
            return Token("COMMENT", comment_text.strip(), start_line, start_col)
        elif self._match("(!"):
            # multi-line comment until !)
            comment_text = ""
            while True:
                if self._peek() is None:
                    raise SimpleLangLexerError(f"Unterminated multi-line comment at line {start_line}, col {start_col}")
                # check if we find '!)'
                if self._match("!)"):
                    break
                comment_text += self._advance()
            return Token("COMMENT", comment_text.strip(), start_line, start_col)
        else:
            # not actually a comment, revert or throw error
            raise SimpleLangLexerError(f"Invalid comment start at line {start_line}, col {start_col}")

    def _read_operator_or_punctuation(self):
        """Attempt to match multi-char operators first, then single-char."""
        start_line, start_col = self.line, self.column

        # Try 2-char operators
        two_char = self.source[self.position:self.position+2]
        if two_char in self.OPERATORS:
            self._advance()
            self._advance()
            return Token("OPERATOR", two_char, start_line, start_col)

        # Try single-char operator
        one_char = self._peek()
        if one_char in self.OPERATORS:
            self._advance()
            return Token("OPERATOR", one_char, start_line, start_col)

        # Check punctuation
        if one_char in self.PUNCTUATION:
            self._advance()
            return Token("PUNCTUATION", one_char, start_line, start_col)

        # If no match, it's an error
        raise SimpleLangLexerError(f"Unknown symbol '{one_char}' at line {start_line}, col {start_col}")

    def get_tokens(self):
        tokens = []
        while self.position < self.length:
            self._skip_whitespace()
            if self.position >= self.length:
                break

            ch = self._peek()

            # Comments
            if self.source[self.position:].startswith("!!") or self.source[self.position:].startswith("(!"):
                self._read_comment()
                # In many lexers, we'd skip or store comments. We'll store them here.
                #tokens.append(comment_token)
                continue

            # String literal
            if ch == '"':
                string_token = self._read_string_literal()
                tokens.append(string_token)
                continue

            # Number
            if ch.isdigit():
                number_token = self._read_number()
                tokens.append(number_token)
                continue

            # Identifier or keyword
            if ch.isalpha() or ch == "_":
                ident_token = self._read_identifier_or_keyword()
                tokens.append(ident_token)
                continue

            # Operators/punctuation
            op_token = self._read_operator_or_punctuation()
            tokens.append(op_token)

        return tokens
