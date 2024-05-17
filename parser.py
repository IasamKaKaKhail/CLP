import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt5.QtGui import QFont
import ply.lex as lex
import ply.yacc as yacc

class ParserGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setup_lexer()
        self.setup_parser()

    def initUI(self):
        self.setWindowTitle('Code Parser')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        
        # Text box for code input
        self.code_input = QTextEdit(self)
        self.code_input.setFont(QFont('Courier', 12))
        layout.addWidget(QLabel('Input Code:'))
        layout.addWidget(self.code_input)
        
        # Buttons layout
        buttons_layout = QHBoxLayout()
        
        # Tokenize button
        self.tokenize_button = QPushButton('Tokenize', self)
        self.tokenize_button.clicked.connect(self.tokenize_code)
        buttons_layout.addWidget(self.tokenize_button)
        
        # Check Syntax button
        self.check_syntax_button = QPushButton('Check Syntax', self)
        self.check_syntax_button.clicked.connect(self.check_syntax)
        buttons_layout.addWidget(self.check_syntax_button)
        
        # Parse Tree button
        self.parse_tree_button = QPushButton('Show Parse Tree', self)
        self.parse_tree_button.clicked.connect(self.show_parse_tree)
        buttons_layout.addWidget(self.parse_tree_button)
        
        # Execute button
        self.execute_button = QPushButton('Execute', self)
        self.execute_button.clicked.connect(self.execute_code)
        buttons_layout.addWidget(self.execute_button)
        
        layout.addLayout(buttons_layout)
        
        # Error Logger
        self.error_logger = QTextEdit(self)
        self.error_logger.setFont(QFont('Courier', 12))
        self.error_logger.setReadOnly(True)
        self.error_logger.setStyleSheet('color: red;')
        layout.addWidget(QLabel('Error Logger:'))
        layout.addWidget(self.error_logger)
        
        # Result Display
        self.result_display = QTextEdit(self)
        self.result_display.setFont(QFont('Courier', 12))
        self.result_display.setReadOnly(True)
        layout.addWidget(QLabel('Result:'))
        layout.addWidget(self.result_display)
        
        self.setLayout(layout)

    def setup_lexer(self):
        # Define tokens
        tokens = (
            'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN'
        )

        # Token rules
        t_PLUS = r'\+'
        t_MINUS = r'-'
        t_TIMES = r'\*'
        t_DIVIDE = r'/'
        t_LPAREN = r'\('
        t_RPAREN = r'\)'

        def t_NUMBER(t):
            r'\d+'
            t.value = int(t.value)
            return t

        t_ignore = ' \t'

        def t_newline(t):
            r'\n+'
            t.lexer.lineno += len(t.value)

        def t_error(t):
            self.log_error(f"Illegal character '{t.value[0]}'")
            t.lexer.skip(1)

        self.lexer = lex.lex()
        self.lexer.tokens = tokens
        self.lexer.t_PLUS = t_PLUS
        self.lexer.t_MINUS = t_MINUS
        self.lexer.t_TIMES = t_TIMES
        self.lexer.t_DIVIDE = t_DIVIDE
        self.lexer.t_LPAREN = t_LPAREN
        self.lexer.t_RPAREN = t_RPAREN
        self.lexer.t_NUMBER = t_NUMBER
        self.lexer.t_ignore = t_ignore
        self.lexer.t_newline = t_newline
        self.lexer.t_error = t_error

    def setup_parser(self):
        tokens = self.lexer.tokens

        def p_expression_plus(p):
            'expression : expression PLUS term'
            p[0] = p[1] + p[3]

        def p_expression_minus(p):
            'expression : expression MINUS term'
            p[0] = p[1] - p[3]

        def p_expression_term(p):
            'expression : term'
            p[0] = p[1]

        def p_term_times(p):
            'term : term TIMES factor'
            p[0] = p[1] * p[3]

        def p_term_divide(p):
            'term : term DIVIDE factor'
            p[0] = p[1] / p[3]

        def p_term_factor(p):
            'term : factor'
            p[0] = p[1]

        def p_factor_number(p):
            'factor : NUMBER'
            p[0] = p[1]

        def p_factor_expr(p):
            'factor : LPAREN expression RPAREN'
            p[0] = p[2]

        def p_error(p):
            if p:
                self.log_error(f"Syntax error at '{p.value}'")
            else:
                self.log_error("Syntax error at EOF")

        self.parser = yacc.yacc()

        self.parser.p_expression_plus = p_expression_plus
        self.parser.p_expression_minus = p_expression_minus
        self.parser.p_expression_term = p_expression_term
        self.parser.p_term_times = p_term_times
        self.parser.p_term_divide = p_term_divide
        self.parser.p_term_factor = p_term_factor
        self.parser.p_factor_number = p_factor_number
        self.parser.p_factor_expr = p_factor_expr
        self.parser.p_error = p_error

    def tokenize_code(self):
        code = self.code_input.toPlainText()
        self.clear_error_log()
        self.clear_result_display()
        try:
            self.lexer.input(code)
            tokens = []
            while True:
                tok = self.lexer.token()
                if not tok:
                    break
                tokens.append(str(tok))
            self.log_message("Tokens:\n" + "\n".join(tokens))
        except Exception as e:
            self.log_error(str(e))

    def check_syntax(self):
        code = self.code_input.toPlainText()
        self.clear_error_log()
        try:
            self.lexer.input(code)
            for token in self.lexer:
                pass
            self.log_message("No syntax errors found.")
        except Exception as e:
            self.log_error(str(e))

    def execute_code(self):
        code = self.code_input.toPlainText()
        self.clear_error_log()
        self.clear_result_display()
        try:
            result = self.parser.parse(code, lexer=self.lexer)
            self.log_message(f"Result: {result}")
        except Exception as e:
            self.log_error(str(e))

    def show_parse_tree(self):
        code = self.code_input.toPlainText()
        self.clear_error_log()
        try:
            result = self.parser.parse(code, lexer=self.lexer)
            self.log_message(f"Parse tree:\n{result}")
        except Exception as e:
            self.log_error(str(e))

    def log_error(self, message):
        self.error_logger.append(message + '\n')

    def log_message(self, message):
        self.result_display.append(message + '\n')

    def clear_error_log(self):
        self.error_logger.clear()

    def clear_result_display(self):
        self.result_display.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ParserGUI()
    gui.show()
    sys.exit(app.exec_())
