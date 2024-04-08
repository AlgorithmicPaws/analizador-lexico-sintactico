import re

class Automaton:
    """
    Class representing a Deterministic Finite Automaton (DFA).
    """

    def __init__(self, states, alphabet, initial_state, accepting_states, transitions):
        """
        Initialize the DFA with states, alphabet, initial state, accepting states, and transitions.

        Parameters:
        states (list): List of states in the DFA.
        alphabet (list): List of symbols in the alphabet of the DFA.
        initial_state (str): The initial state of the DFA.
        accepting_states (list): List of accepting states in the DFA.
        transitions (list): List of tuplets representing transitions in the DFA. 
                            

        Attributes:
        states (list): List of states in the DFA.
        alphabet (list): List of symbols in the alphabet of the DFA.
        initial_state (str): The initial state of the DFA.
        accepting_states (list): List of accepting states in the DFA.
        transitions (dict): Dictionary representing transitions in the DFA.
        row (int): Current row index for processing input tokens.
        column (int): Current column index for processing input tokens.
        token_list (list): List to store processed tokens.
        """
        self.states = states
        self.alphabet = alphabet
        self.initial_state = initial_state
        self.accepting_states = accepting_states
        self.transitions = transitions
        self.row = 1
        self.column = 0
        self.token_list = []

    def counter(self, symbol):
        """
        Process the symbol to count rows and colums
        """
        if symbol == '\n':
            self.row += 1
            self.column = 0
        elif symbol == '\t':
            self.column += 4
        else:
            self.column += 1

    def rerun(self, input_string):
        """
        Rerun the DFA on the input string until fully processed.
        """
        actual_input = self.run(input_string)
        while True:    
            if actual_input == True:
                return True
            elif actual_input == False:
                return False
            else:
                actual_input = self.run(actual_input)     

    def run(self, input_list):
        current_state = self.initial_state
        expression = ''
        for index in range(len(input_list)):
            symbol = input_list[index]
            self.counter(symbol)
            next_state = None
            for transition in self.transitions:
                if transition[0] == current_state and re.match(transition[1], symbol):
                    state = transition[2]
                    expression += symbol
                    if len(expression) == 1:
                        expression_start_row = self.row
                        expression_start_column = self.column
                    next_state = state
                    break
            current_state = next_state

            if not self.alphabet.match(symbol):
                expression = expression[:-1]
                if len(expression) > 0:
                    self.tokenizer(expression, expression_start_row, expression_start_column, current_state)
                    self.error_tokenizer(self.row,self.column + 1 )
                else:
                    self.error_tokenizer(self.row,self.column)
                return False
            
            if next_state is None:
                self.error_tokenizer(self.row,self.column)
                return False
            
            if index == len(input_list) -1:
                expression = expression[:-1]
                self.tokenizer(expression, expression_start_row, expression_start_column,current_state)
                return True
            
            elif current_state in self.accepting_states:
                if len(expression) > 1: 
                    expression = expression[:-1]
                    self.tokenizer(expression, expression_start_row, expression_start_column, current_state)
                    self.column-= 1
                    if symbol == '\n':
                        self.row-= 1  
                    expression = ''
                    return input_list[index:]
                else:
                    self.tokenizer(expression, expression_start_row, expression_start_column, current_state)
                    expression = ''
                    current_state = self.initial_state
                    return input_list[index:]

    def error_tokenizer(self, start_row, start_column):
        self.token_list.append((start_row, start_column ))
    
    def tokenizer(self, expression, start_row, start_column, final_state):
        keywords= [ 
        'case','match', 'self','False', 'None', 'True', 'and', 'as', 'assert', 'async','await',
        'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 
        'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not',  
        'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield', 
        'abs', 'acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil', 
        'comb', 'copysign', 'cos', 'cosh', 'degrees', 'dist', 'erf', 'erfc', 'exp', 
        'expm1', 'fabs', 'factorial', 'floor', 'fmod', 'frexp', 'fsum', 'gamma', 
        'gcd', 'hypot', 'isclose', 'isfinite', 'isinf', 'isnan', 'isqrt', 'ldexp', 
        'lgamma', 'log', 'log10', 'log1p', 'log2', 'modf', 'perm', 'pi', 'pow', 
        'prod', 'radians', 'remainder', 'sin', 'sinh', 'sqrt', 'tan', 'tanh', 'tau', 
        'trunc', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes', 'callable', 
        'chr', 'classmethod', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod', 
        'enumerate', 'eval', 'exec', 'filter', 'float', 'format', 'frozenset', 'getattr', 
        'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 
        'issubclass', 'iter', 'len', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 
        'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 
        'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 
        'sum', 'super', 'tuple', 'type', 'vars', 'zip', 'Ellipsis', 'NotImplemented' 
        'os', 'sys', 'math', 'random', 'datetime', 're', 'json', 'csv', 'pickle', 'time', 
        'collections', 'itertools', 'functools', 'operator', 'logging', 'pathlib', 'gzip', 'zipfile', 
        'io', 'shutil', 'platform', 'subprocess', 'threading', 'multiprocessing', 'socket', 'http', 'urllib', 
        'ftplib', 'ssl', 'email', 'smtplib', 'imaplib', 'poplib', 'xml', 'html', 'cgi', 'sqlite3', 
        'multiprocessing', 'concurrent', 'asyncio', 'unittest', 'doctest', 'pytest', 'argparse', 'getopt', 
        'configparser', 'logging', 'tkinter', 'pygame', 'pandas', 'numpy', 'matplotlib', 'scipy', 'seaborn', 
        'sklearn', 'tensorflow', 'pytorch', 'flask', 'django', 'sqlalchemy', '_', '__init__'
        ] 
        symbols = {
        '+': 'tk_plus', '-': 'tk_minus', '*': 'tk_asterisk', '**': 'tk_double_asterisk',
        '/': 'tk_slash', '//': 'tk_double_slash', '%': 'tk_percent', '@': 'tk_at',
        '<<': 'tk_left_shift', '>>': 'tk_right_shift', '&': 'tk_ampersand', '|': 'tk_pipe',
        '^': 'tk_caret', '~': 'tk_tilde', ':=': 'tk_walrus',
        '<': 'tk_less_than', '>': 'tk_greater_than', '<=': 'tk_less_than_or_equal_to',
        '>=': 'tk_greater_than_or_equal_to', '==': 'tk_equal_to', '!=': 'tk_not_equal_to',
        '(': 'tk_left_parenthesis', ')': 'tk_right_parenthesis',
        '[': 'tk_left_square_bracket', ']': 'tk_right_square_bracket',
        '{': 'tk_left_curly_brace', '}': 'tk_right_curly_brace',
        ',': 'tk_comma', ':': 'tk_colon', '.': 'tk_dot', ';': 'tk_semicolon', '=': 'tk_equal',
        '->': 'tk_arrow', '+=': 'tk_plus_equal', '-=': 'tk_minus_equal', '*=': 'tk_multiply_equal',
        '/=': 'tk_divide_equal', '//=': 'tk_double_divide_equal', '%=': 'tk_modulus_equal',
        '@=': 'tk_at_equal', '&=': 'tk_and_equal', '|=': 'tk_or_equal', '^=': 'tk_xor_equal',
        '>>=': 'tk_right_shift_equal', '<<=': 'tk_left_shift_equal', '**=': 'tk_double_asterisk_equal',
        '!': 'tk_exclamation', '\\': 'tk_backslash',
        }   
        
        # Determine token type based on final state
        if final_state == 'q5' or final_state == 'q12':
            token_type = "tk_integer"
            self.token_list.append((token_type, expression, start_row, start_column))
        elif final_state == 'q6' or  final_state == 'q52':
            token_type = "tk_float"
            self.token_list.append((token_type, expression, start_row, start_column))
        elif final_state == 'q17':
            token_type = "tk_imaginary"
            self.token_list.append((token_type, expression, start_row, start_column))
        elif final_state == 'q22':
            token_type = "tk_string"
            self.token_list.append((token_type, expression, start_row, start_column))

        elif final_state in ['q19', 'q29', 'q32']:
            # Check for keywords, symbols, or identifiers
            if expression in keywords:
                token_type = expression
                self.token_list.append((token_type, start_row, start_column))
            elif expression in symbols:
                token_type = symbols[expression]
                self.token_list.append((token_type, start_row, start_column))
            else:
                token_type = "Id"
                self.token_list.append((token_type, expression, start_row, start_column))
 
        else:
            return
    


