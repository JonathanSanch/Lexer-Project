import re

# Define the Token class with the required attributes.
class Token:
    def __init__(self, lexeme, token_class, symbol_type, data_type=None, value=None):
        self.lexeme = lexeme
        self.token_class = token_class
        self.symbol_type = symbol_type
        self.data_type = data_type
        self.value = value

    def __str__(self):
        # Convert None fields to empty strings for display
        data_type = self.data_type if self.data_type is not None else ""
        value = self.value if self.value is not None else ""
        return f"{self.lexeme}\t{self.token_class}\t{self.symbol_type}\t{data_type}\t{value}"

# Define the SymbolTable class to manage tokens.
class SymbolTable:
    def __init__(self):
        self.table = {}

    def add_token(self, token):
        self.table[token.lexeme] = token

    def get_token(self, lexeme):
        return self.table.get(lexeme, None)

    def display(self):
        # Define column headers with fixed widths
        headers = ["Lexeme", "Token Class", "SymbolType", "DataType", "Value"]
        widths = [15, 15, 15, 10, 10]  # Set column widths

        # Print header with column widths
        header_row = "".join(f"{header:<{width}}" for header, width in zip(headers, widths))
        print(header_row)
        print("-" * sum(widths))  # Print a line separator

        # Print each token row with aligned columns
        for token in self.table.values():
            # Use empty strings for None fields
            data_type = token.data_type if token.data_type is not None else ""
            value = token.value if token.value is not None else ""
            row = f"{token.lexeme:<15}{token.token_class:<15}{token.symbol_type:<15}{data_type:<10}{value:<10}"
            print(row)

# Define the Lexer class to process input text and generate tokens.
class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.symbol_table = SymbolTable()
        self.current_position = 0
        self.last_data_type = None  # Track the most recent data type for declarations

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
                
                # Assign custom token classes based on lexeme and type
                token_class = self.assign_custom_token_class(token_class, lexeme)
                
                data_type, value = self.determine_data_type_and_value(token_class, lexeme)
                symbol_type = self.determine_symbol_type(token_class)
                token = Token(lexeme, token_class, symbol_type, data_type=data_type, value=value)
                self.symbol_table.add_token(token)
                self.current_position += len(lexeme)

                # Update last_data_type if lexeme is a declaration keyword
                if token_class == "Keyword" and lexeme in ["int", "bool", "float", "char"]:
                    self.last_data_type = lexeme
                elif token_class == "Identifier" and self.last_data_type:
                    # Assign last_data_type to identifiers declared right after a type keyword
                    token.data_type = self.last_data_type
                    self.last_data_type = None  # Reset after assignment

                return token

        # If no token matches, print a warning and move forward
        print(f"Warning: Unexpected character '{self.input_text[self.current_position]}' at position {self.current_position}")
        self.current_position += 1  # Move forward to continue lexing

    def assign_custom_token_class(self, token_class, lexeme):
        # Update the token class based on specific lexeme requirements
        if token_class == "Keyword":
            if lexeme == "while":
                return "TokWhile"
            elif lexeme in ["if", "else"]:
                return "TokIf"
            # Keep `Keyword` as is for other keywords like "int", "float", etc.
        elif token_class in ["Integer", "Char", "Boolean"]:
            return "TokLiteral"  # Assign TokLiteral to Integer, Char, and Boolean
        return token_class

    def determine_data_type_and_value(self, token_class, lexeme):
        # Determine the data type and value based on the token class and lexeme
        if token_class == "TokLiteral":
            if re.fullmatch(r'\b\d+\b', lexeme):  # Integer literal
                return "int", int(lexeme)
            elif re.fullmatch(r'\b\d+\.\d+\b', lexeme):  # Float literal
                return "float", float(lexeme)
            elif lexeme == "true" or lexeme == "false":  # Boolean literal
                return "bool", True if lexeme == "true" else False
            elif len(lexeme) == 3 and lexeme[0] == "'" and lexeme[2] == "'":  # Char literal (e.g., 'A')
                return "char", lexeme[1]
        elif token_class == "Identifier" and self.last_data_type:
            return self.last_data_type, None  # No initial value for identifier declarations
        return None, None  # Default for other tokens

    def determine_symbol_type(self, token_class):
        # Map token classes to symbol types based on the requirements
        if token_class in ["Keyword", "Identifier", "TokLiteral"]:
            return "Variable" if token_class == "Identifier" else "Literal"
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
def main():
    # Read input file
    with open('input.txt', 'r') as file:
        input_text = file.read()

    # Initialize lexer and tokenize the input
    lexer = Lexer(input_text)
    lexer.tokenize()

    # Display the symbol table
    lexer.display_symbol_table()

if __name__ == "__main__":
    main()