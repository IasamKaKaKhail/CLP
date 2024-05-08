import re

class Tokenizer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.tokens = []
        self.pos = 0
        self.tokenize()

    def tokenize(self):
        token_specification = [
            ('NUMBER', r'\d+(\.\d*)?'),  # Integer or decimal number
            ('ASSIGN', r'='),            # Assignment operator
            ('END', r';'),               # Statement terminator
            ('ID', r'[A-Za-z]+'),        # Identifiers
            ('OP', r'[\+\-\*/]'),        # Arithmetic operators
            ('LPAREN', r'\('),           # Left Parenthesis
            ('RPAREN', r'\)'),           # Right Parenthesis
            ('SKIP', r'[ \t]+'),         # Skip over spaces and tabs
            ('M_COMMENT', r'/\*.*?\*/'), # Multi-line comments
            ('S_COMMENT', r'//.*'),      # Single-line comments
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        get_token = re.compile(tok_regex, re.DOTALL).finditer

        for mo in get_token(self.input_string):
            kind = mo.lastgroup
            value = mo.group(kind)
            if kind in ['SKIP', 'S_COMMENT', 'M_COMMENT']:
                continue
            self.tokens.append((kind, value))

    def next_token(self):
        if self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        return None

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def get_tokens(self):
        return self.tokens

class Parser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.tokens = tokenizer.get_tokens()
        self.pos = 0
    
    def parse(self):
        if not self.tokenizer.tokens:
            return None
        return self.expression()

    def expression(self):
        tokens = []
        token = self.tokenizer.next_token()
        while token and token[0] != 'END':
            tokens.append(token)
            token = self.tokenizer.next_token()
        return tokens

    # def add_sub(self):
    #     result = self.mul_div()
    #     while self.pos < len(self.tokens):
    #         token = self.tokens[self.pos]
    #         if token[0] in ('ADD', 'SUB'):
    #             self.pos += 1
    #             if token[0] == 'ADD':
    #                 result += self.mul_div()
    #             elif token[0] == 'SUB':
    #                 result -= self.mul_div()
    #         else:
    #             break
    #     return result
    
    # def mul_div(self):
    #     result = self.factor()
    #     while self.pos < len(self.tokens):
    #         token = self.tokens[self.pos]
    #         if token[0] in ('MUL', 'DIV'):
    #             self.pos += 1
    #             if token[0] == 'MUL':
    #                 result *= self.factor()
    #             elif token[0] == 'DIV':
    #                 divisor = self.factor()
    #                 if divisor != 0:
    #                     result /= divisor
    #                 else:
    #                     raise ValueError("Division by zero")
    #         else:
    #             break
    #     return result

    # def factor(self):
    #     token = self.tokens[self.pos]
    #     if token[0] == 'NUMBER':
    #         self.pos += 1
    #         return int(token[1])
    #     elif token[0] == 'LPAREN':
    #         self.pos += 1
    #         result = self.expression()
    #         if self.tokens[self.pos][0] == 'RPAREN':
    #             self.pos += 1
    #             return result
    #         else:
    #             raise Exception("Unmatched parenthesis")
    #     else:
    #         raise Exception("Invalid syntax")

def accept_input():
    user_input = input("Enter an expression: ")
    return user_input

def main():
    print("Enter your expression (type 'END;' to exit):")
    while True:
        try:
            input_string = input("> ")
            if input_string.strip() == 'END;':
                break
            tokenizer = Tokenizer(input_string)
            print("Tokenizer Output:", tokenizer.tokens)
            parser = Parser(tokenizer)
            parse_tree = parser.parse()
            print("Parse Tree:", parse_tree)
        except Exception as e:
            print("Error:", str(e))

if __name__ == "__main__":
    main()

# def main():
#     user_input = accept_input()
#     tokenizer = Tokenizer()
#     tokenizer.tokenize_input(user_input)
#     parser = Parser(tokenizer)
#     try:
#         result = parser.expression()
#         print("Result:", result)
#     except Exception as e:
#         print("Error:", str(e))

# if __name__ == "__main__":
#     main()
