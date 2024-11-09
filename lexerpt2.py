import re

# Define the Token class with the required attributes.
class Token:
    def __init__(self, lexeme, token_class, symbol_type, data_type=None, value=None, scope="Global"):
        self.lexeme = lexeme
        self.token_class = token_class
        self.symbol_type = symbol_type
        self.data_type = data_type
        self.value = value
        self.scope = scope

    def __str__(self):
        return f"{self.lexeme}\t{self.token_class}\t{self.symbol_type}\t{self.data_type}\t{self.value}\t{self.scope}"

# Define the SymbolTable class to manage tokens.
class SymbolTable:
    def __init__(self):
        self.table = {}

    def add_token(self, token):
        self.table[token.lexeme] = token

    def get_token(self, lexeme):
        return self.table.get(lexeme, None)

    def display(self):
        print("Lexeme\tToken Class\tSymbol Type\tData Type\tValue\tScope")
        print("-------------------------------------------------------------")
        for token in self.table.values():
            print(token)

# Define the Lexer class to process input text and generate tokens.
class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.symbol_table = SymbolTable()
        self.current_position = 0

        # Regular expressions for various token types based on Clite Grammar
        self.token_patterns = {
            'Keyword': r'\b(int|bool|float|char|if|else|while|main)\b',
            'Identifier': r'\b[a-zA-Z_]\w*\b',
            'Integer': r'\b\d+\b',
            'Float': r'\b\d+\.\d+\b',
            'Boolean': r'\b(true|false)\b',
            'Char': r"'.'",
            'RelOp': r'<=|>=|<|>',
            'EquOp': r'==|!=',
            'AddOp': r'\+|\-',
            'MulOp': r'\*|\/|%',
            'UnaryOp': r'\!|\-',
            'Assignment': r'=',
            'Delimiter': r'\{|\}|\(|\)|;'
        }

    def get_next_token(self):
        # Skip whitespace and comments
        while self.current_position < len(self.input_text) and self.input_text[self.current_position].isspace():
            self.current_position += 1

        if self.current_position >= len(self.input_text):
            return None

        # Check each pattern to find the longest match at the current position
        for token_class, pattern in self.token_patterns.items():
            regex = re.compile(pattern)
            match = regex.match(self.input_text, self.current_position)
            if match:
                lexeme = match.group(0)
                symbol_type = self.determine_symbol_type(token_class)
                token = Token(lexeme, token_class, symbol_type)
                self.symbol_table.add_token(token)
                self.current_position += len(lexeme)
                return token

        # If no token matches, raise an error
        raise ValueError(f"Unexpected character at position {self.current_position}")

    def determine_symbol_type(self, token_class):
        # Map token classes to symbol types based on the requirements
        if token_class in ["Keyword", "Identifier", "Char", "Integer", "Float", "Boolean"]:
            return token_class
        elif token_class in ["RelOp", "EquOp", "AddOp", "MulOp", "UnaryOp", "Assignment"]:
            return "Operator"
        elif token_class == "Delimiter":
            return "Symbol"
        else:
            return "Unknown"

    def tokenize(self):
        tokens = []
        while self.current_position < len(self.input_text):
            token = self.get_next_token()
            if token:
                tokens.append(token)
        return tokens

    def display_symbol_table(self):
        self.symbol_table.display()

# Read input from a file and tokenize
# Read input file
with open('input.txt', 'r') as file:
    input_text = file.read()

# Initialize lexer and tokenize the input
lexer = Lexer(input_text)
lexer.tokenize()

# Display the symbol table
lexer.display_symbol_table()

print("Hello World")