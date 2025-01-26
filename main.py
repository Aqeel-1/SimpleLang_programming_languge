from lexer import SimpleLangLexer, SimpleLangLexerError
from parser import SimpleLangParser, SimpleLangParserError

source_code = r"""
whole add(whole a, whole b) {
    output a + b;
}

(! 
this is commint
sakldsali
!)

whole main() {
    text message = "The result is: ";
    whole result = add(5, 10);
    show(message + result);
    
}
"""

# 1. Lexing
lexer = SimpleLangLexer(source_code)
tokens = lexer.get_tokens()
print("=== TOKENS ===")
for t in tokens:
    print(t)

# 2. Parsing
parser = SimpleLangParser(tokens)
try:
    ast = parser.parse()
    print("\n=== AST ===")
    print(ast)
except SimpleLangParserError as e:
    print("Parser Error:", e)
except SimpleLangLexerError as e:
    print("Lexer Error:", e)