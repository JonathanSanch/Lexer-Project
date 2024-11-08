# Define token types and keywords, operators, symbols
KEYWORDS = {'int', 'bool', 'float', 'char', 'if', 'else', 'while', 'return'}
OPERATORS = {'=', '==', '!=', '+', '-', '*', '/', '%', '<', '<=', '>', '>='}
SYMBOLS = {'{', '}', ';', '(', ')'}


# Token class to represent each token with type, lexeme, and optional value
class Token:
    def __init__(self, token_type, lexeme, value=None):
        self.type = token_type
        self.lexeme = lexeme
        self.value = value

    def __repr__(self):
        return f"Token(type='{self.type}', lexeme='{self.lexeme}', value={self.value})"


# Initialize an empty symbol table
symbol_table = {}


# Lexer class to perform lexical analysis
class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.position = 0
        self.tokens = []

    def get_char(self):
        """Get the current character and advance the position."""
        if self.position < len(self.input_text):
            char = self.input_text[self.position]
            self.position += 1
            return char
        return None  # End of input

    def peek(self):
        """Look at the next character without moving the position."""
        if self.position < len(self.input_text):
            return self.input_text[self.position]
        return None

    def recognize_identifier(self, start_char):
        """Recognize identifiers and keywords."""
        lexeme = start_char
        while self.peek() and (self.peek().isalnum() or self.peek() == '_'):
            lexeme += self.get_char()
        
        if lexeme in KEYWORDS:
            return Token('KEYWORD', lexeme)
        else:
            # Add to symbol table if it's an identifier
            if lexeme not in symbol_table:
                symbol_table[lexeme] = {'type': 'Identifier', 'value': None}
            return Token('IDENTIFIER', lexeme)

    def recognize_number(self, start_char):
        """Recognize integer and floating-point numbers."""
        lexeme = start_char
        is_float = False

        while self.peek() and self.peek().isdigit():
            lexeme += self.get_char()
        
        # Check if it’s a float by looking for a decimal point
        if self.peek() == '.':
            is_float = True
            lexeme += self.get_char()  # Include the dot
            while self.peek() and self.peek().isdigit():
                lexeme += self.get_char()

        token_type = 'FLOAT' if is_float else 'INTEGER'
        return Token(token_type, lexeme, float(lexeme) if is_float else int(lexeme))

    def recognize_operator(self, start_char):
        """Recognize operators, including multi-character operators."""
        lexeme = start_char
        if lexeme + self.peek() in OPERATORS:
            lexeme += self.get_char()
        return Token('OPERATOR', lexeme)
    
    def recognize_symbol(self, char):
        """Recognize symbols like braces, semicolons, etc."""
        return Token('SYMBOL', char)

    def tokenize(self):
        """Tokenize the entire input into a list of tokens."""
        while (current_char := self.get_char()) is not None:
            if current_char.isspace():
                continue  # Skip whitespace
            elif current_char in SYMBOLS:
                self.tokens.append(self.recognize_symbol(current_char))
            elif current_char in OPERATORS:
                self.tokens.append(self.recognize_operator(current_char))
            elif current_char.isalpha():
                self.tokens.append(self.recognize_identifier(current_char))
            elif current_char.isdigit():
                self.tokens.append(self.recognize_number(current_char))
            else:
                print(f"Unexpected character '{current_char}'")
        
        return self.tokens


# Example usage
input_text = "int x = 10; int y = 10; String hello = 'hello' while (x > 5) { x = x - 1; }"
lexer = Lexer(input_text)
tokens = lexer.tokenize()

for token in tokens:
    print(token)

print("Symbol Table:", symbol_table)