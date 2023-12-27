# supp.py
###############################
# DIGITS
###############################

DIGITS = '0123456789'

###############################
# ERRORS
##############################

class Error:
    def __init__(self, error_name, details):
        self.error_name = error_name
        self.details = details

    def as_string(self):
        result = f'{self.error_name}: {self.details}'
        return result

class IllegalCharError(Error):
    def __init__(self, details):
        super().__init__('Illegal Character', details)

###############################
# TOKENS
###############################

TT_INT      = 'INT'
TT_FLOAT    = 'FLOAT'
TT_LPAREN   = 'LPAREN'
TT_RPAREN   = 'RPAREN'
TT_SCOLON   = 'SCOLON'
TT_COLON    = 'COLON'
TT_OCBRACE  = 'OCBRACE'
TT_CCBRACE  = 'CCBRACE'

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

###############################
# LEXER
###############################

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = -1
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char == '(':
                tokens.append(Token(TT_LPAREN))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(TT_RPAREN))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(TT_SCOLON))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(TT_COLON))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(TT_OCBRACE))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(TT_CCBRACE))
                self.advance()
            else: # return an error message
                char = self.current_char
                self.advance()
                return [], IllegalCharError("'" + char + "'")

        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char is not None and self.current_char in DIGITS + '.':
            if self.current_char == '.':
                if dot_count:
                    break
                dot_count = 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, str(num_str))
        else:
            return Token(TT_FLOAT, str(num_str))

###############################
# RUN
###############################

def run(text):
    lexer = Lexer(text)
    tokens, error = lexer.make_tokens()

    return tokens, error.as_string() if error else None

