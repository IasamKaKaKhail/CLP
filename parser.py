import re

class Tokenizer:
    def __init__(self):
        self.tokens = []

    def tokenize_input(self, input_string):
        # Define regular expressions for different token types
        patterns = [
            ('NUMBER', r'\d+'),  
            ('LETTER', r'[a-zA-Z]'),
            ('STRING', r'\".*?\"'),
            ('OPERATOR', r'[\+\-\*/]'),
            ('LPAREN', r'\('),
            ('RPAREN', r'\)'),
            ('WHITESPACE', r'\s+')
        ]

        # Combine patterns into a single regular expression
        combined_pattern = '|'.join('(?P<%s>%s)' % pair for pair in patterns)

        # Tokenize the input string
        for match in re.finditer(combined_pattern, input_string):
            token_type = match.lastgroup
            token_value = match.group(token_type)
            if token_type != 'WHITESPACE':
                self.tokens.append((token_type, token_value))

    def get_tokens(self):
        return self.tokens

def accept_input():
    user_input = input("Enter an expression: ")
    return user_input

def main():
    tokenizer = Tokenizer()
    while True:
        try:
            user_input = accept_input()
            tokenizer.tokenize_input(user_input)
            tokens = tokenizer.get_tokens()
            print("Tokens:", tokens)
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()
