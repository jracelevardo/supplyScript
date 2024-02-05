
import os
from strings_with_arrows import *

###############################
# DIGITS
###############################

DIGITS = '0123456789'

###############################
# LETTERS
###############################

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

###############################
# SYMBOLS
###############################

QUOTATIONS = {"'", '"'}
PARENTHESES = '()'
CURLYBRACE = '{}'
SPECIALCHAR = '.;@#$₱&`_|'

###############################
# OPERATORS
###############################
ASSIGNOPRTR = {'=', ':'}
ARITHMETICOPRTR = {'+', '-', '*', '/', '%', '^', '/.'}
BOOLOPRTR = {"==", "!=", ">", "<", "<=", ">=", "&&", "||", "!"}

###############################
# CLASS TYPES
###############################
CLASS_TYPES = {'Product', 'Supplier', 'Order'}

###############################
# ATTRIBUTES (KEYWORDS)
###############################
ATTRIBUTES = {'name', 'supplier', 'product', 'quantity', 'location', 'weight', 'unitPrice', 'deliveryDate'}

###############################
# RESERVED WORDS
###############################
RESERVED_WORDS = {'alert', 'undo', 'exec', 'update', 'optimize', 'show', 'allowArithmetic'}


###############################
# ERRORS
###############################

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
        

class InvalidSyntaxError(Error):
		def __init__(self, pos_start, pos_end, details=''):
				super().__init__(pos_start, pos_end, 'Invalid Syntax', details)


class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)


###############################
# TOKENS
###############################

TT_INT                  = 'INT:                           '
TT_FLOAT                = 'FLOAT:                         '
TT_LPAREN               = 'LEFTPAREN:                      ' + '('
TT_RPAREN               = 'RIGHTPAREN:                    ' + ')'
TT_SCOLON               = 'SEMICOLON:                      ' + ';'
TT_COLON                = 'COLON:                         ' + ':'
TT_OCBRACE              = 'OPENCURLBRACE:                 ' + '{'
TT_CCBRACE              = 'CLOSECURLBRACE:                ' + '}'
TT_DQUOTATION           = 'DOUBLEQUOTATION:               ' + '"'
TT_SQUOTATION           = 'SINGLEQUOTATION:               ' + "'"
TT_ASSIGNMENT_EQUAL     = 'ASSIGNOPRTR_EQUAL:         ' + '='
TT_ASSIGNMENT_COLON     = 'ASSIGNOPRTR_COLON:          ' + ':'
TT_STRLITERAL           = 'STRINGLITERAL:                 '
TT_IDENTIFIER           = 'IDENTIFIER:                    '
TT_ADD                  = 'ADDSYMBOL:                     ' + '+'
TT_SUB                  = 'SUBTRACTSYMBOL:                ' + '-'
TT_MUL                  = 'MULTIPLYSYMBOL:          ' + '*'
TT_DIV                  = 'DIVISIONSYMBOL:                ' + '/'
TT_CLASSTYPE            = 'CLASSTYPE:                    '
TT_ATTRIBUTE            = 'ATTRIBUTE:                     '
TT_RESERVEDWORD         = 'RESERVEDWORD:                  '
TT_SPECIALCHAR          = 'SPECIALCHAR:                '
TT_SINGLECOMMENT        = 'SINGLECOMMENT:                 ' + '//'
TT_STARTCOMMENT         = 'STARTCOMMENT:                  ' + '/*'
TT_ENDCOMMENT           = 'ENDCOMMENT:                    ' + '*/'
TT_COMMENT              = 'COMMENT:                       '
TT_MOD                  = 'MOD:                                 ' + '%'
TT_EXP                  = 'EXP:                                   ' + '^'
TT_FLOOR                = 'FLOOR:                         ' + '/.'
TT_EQUIVAL              = 'EQUIVAL:                       ' + '=='
TT_NOTEQUAL             = 'NOTEQUAL:                      ' + '!='
TT_GREATER              = 'GREATER:                       ' + '>'
TT_LESS                 = 'LESS:                          ' + '<'
TT_LEQUAL               = 'LEQUAL:                        ' + '<='
TT_GEQUAL               = 'GEQUAL:                        ' + '>='
TT_AND                  = 'AND:                           ' + '&&'
TT_OR                   = 'OR:                            ' + '||'
TT_NOT                  = 'NOT:                                   ' + '!'
TT_EOF = 'EOF'


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'


###############################
# LEXER
###############################

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(-1, 0, -1, '', text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char is not None:
            if self.current_char in '\t':
                self.advance()
            elif self.current_char in '\n':
                self.advance()
            elif self.current_char in " ":
                self.advance()

            # Check for single-line comment
            elif self.current_char == '/' and self.peek() == '/':
                comment_text = self.make_single_line_comment()
                tokens.append(Token(TT_SINGLECOMMENT))
                tokens.append(Token(TT_COMMENT, comment_text))

            # Check for multi-line comment
            elif self.current_char == '/' and self.peek() == '*':
                comment_text = self.make_multi_line_comment()
                tokens.append(Token(TT_STARTCOMMENT))
                tokens.append(Token(TT_COMMENT, comment_text))
                tokens.append(Token(TT_ENDCOMMENT))

            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())

            elif self.current_char in QUOTATIONS:
                result = self.make_string_literal()
                if isinstance(result, Token):
                    tokens.append(result)
                else:
                    return tokens, result  # Return the error along with tokens

            elif self.current_char in PARENTHESES:
                if self.current_char == '(':
                    tokens.append(Token(TT_LPAREN))
                    self.advance()
                elif self.current_char == ')':
                    tokens.append(Token(TT_RPAREN))
                    self.advance()
            elif self.current_char in CURLYBRACE:
                if self.current_char == '{':
                    tokens.append(Token(TT_OCBRACE))
                    self.advance()
                elif self.current_char == '}':
                    tokens.append(Token(TT_CCBRACE))
                    self.advance()

            elif self.current_char in (ASSIGNOPRTR or BOOLOPRTR or SPECIALCHAR):
                if self.current_char == '=':
                    if self.peek() == '=':
                        tokens.append(Token(TT_EQUIVAL))
                        self.advance()
                        self.advance()
                    else:
                        tokens.append(Token(TT_ASSIGNMENT_EQUAL))
                        self.advance()
                elif self.current_char == ':':
                    tokens.append(Token(TT_ASSIGNMENT_COLON))
                    self.advance()

            elif self.current_char == ';':
                tokens.append(Token(TT_SCOLON))
                self.advance()


            elif self.current_char == '&':
                if self.peek() == '&':
                    tokens.append(Token(TT_AND))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token(TT_SPECIALCHAR, '&'))
                    self.advance()


            elif self.current_char == '|':
                if self.peek() == '|':
                    tokens.append(Token(TT_OR))
                    self.advance()
                    self.advance()
                else:
                    tokens.append(Token(TT_SPECIALCHAR, '|'))
                    self.advance()

            elif self.current_char in SPECIALCHAR:
                tokens.append(self.make_specialchar())

            elif self.current_char in ARITHMETICOPRTR:
                tokens.append(self.make_arithmetic_operator())

            elif self.current_char in BOOLOPRTR:
                if self.current_char == '!':
                    if self.peek() == '=':
                        tokens.append(Token(TT_NOTEQUAL))
                        self.advance()
                        self.advance()
                    else:
                        tokens.append(Token(TT_NOT))
                        self.advance()
                elif self.current_char == '<':
                    if self.peek() == '=':
                        tokens.append(Token(TT_LEQUAL))
                        self.advance()
                        self.advance()
                    else:
                        tokens.append(Token(TT_LESS))
                        self.advance()
                elif self.current_char == '>':
                    if self.peek() == '=':
                        tokens.append(Token(TT_GEQUAL))
                        self.advance()
                        self.advance()
                    else:
                        tokens.append(Token(TT_GREATER))
                        self.advance()

            else:  # return an error message
                char = self.current_char
                self.advance()
                return tokens, IllegalCharError("'" + char + "'")

        tokens.append(Token(TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        num_str = ''
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None and (self.current_char in DIGITS or self.current_char == '.'):
            if self.current_char == '.':
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += '.'
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)


    def make_arithmetic_operator(self):
        oprtr_str = self.current_char

        if oprtr_str =='/':
            if self.peek()=='.':
                oprtr_str +=self.peek()
                self.advance()
                self.advance()
                return Token(TT_FLOOR)
        self.advance()

        if oprtr_str == '+':
            return Token(TT_ADD)
        elif oprtr_str == '-':
            return Token(TT_SUB)
        elif oprtr_str == '*':
            return Token(TT_MUL)
        elif oprtr_str == '/':
            return Token(TT_DIV)
        elif oprtr_str == '%':
            return Token(TT_MOD)
        elif oprtr_str == '^':
            return Token(TT_EXP)
        elif oprtr_str == '/.':
            return Token(TT_FLOOR)

    def peek(self):
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None

    def make_single_line_comment(self):
        self.advance()  # Move past the '/'
        self.advance()  # Move past the '/'
        comment_text = ''
        while self.current_char is not None and self.current_char != '\n':
            comment_text += self.current_char
            self.advance()
        return comment_text

    def make_multi_line_comment(self):
        self.advance()  # Move past the '/'
        self.advance()  # Move past the '*'
        comment_text = ''
        while self.current_char is not None and not (self.current_char == '*' and self.peek() == '/'):
            if self.current_char=='\n':
                comment_text += self.current_char
            else:
                comment_text += self.current_char
            self.advance()

        if self.current_char is None:
            raise IllegalCharError(
                f"Unterminated multi-line comment starting at position {self.pos - len(comment_text)}")
        self.advance()  # Move past the '*'
        self.advance()  # Move past the '/'
        return comment_text

    def make_identifier(self):
        id_str = ''
        # A name must begin with a letter (A-Z or a-z), dollar sign ($), or an underscore (_)
        if self.current_char is not None and self.current_char in LETTERS + '$_':
            id_str += self.current_char
            self.advance()
        else:
            return Token(TT_IDENTIFIER, None)  # Invalid identifier

        # Subsequent characters may be letters, digits, underscores, or dollar signs
        while self.current_char is not None and self.current_char in LETTERS + DIGITS + '_$':
            id_str += self.current_char
            self.advance()

        # Identify class type, attribute, or reserved word
        if id_str in CLASS_TYPES:
            return Token(TT_CLASSTYPE, f' {id_str}')
        elif id_str in ATTRIBUTES:
            return Token(TT_ATTRIBUTE, f' {id_str}')
        elif id_str in RESERVED_WORDS:
            return Token(TT_RESERVEDWORD, f' {id_str}')
        elif id_str == 'execute':
            r_word = id_str[:4]
            return Token(TT_RESERVEDWORD, f' {r_word} | NOISEWORD: ute')
        elif id_str == 'updateInventory':
            r_word = id_str[:6]
            return Token(TT_RESERVEDWORD, f' {r_word} | NOISEWORD: Inventory')
        elif id_str == 'optimizeInventoryLevels':
            r_word = id_str[:8]
            return Token(TT_RESERVEDWORD, f' {r_word} | NOISEWORD: InventoryLevels')
        else:
            return Token(TT_IDENTIFIER, id_str)

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

    def make_string_literal(self):
        quote_type = self.current_char
        self.advance()
        str_literal = ""
        while self.current_char is not None and self.current_char != quote_type:
            str_literal += self.current_char
            self.advance()
        if self.current_char == quote_type:
            self.advance()
            return Token(TT_STRLITERAL, str_literal)
        else:
            return IllegalCharError(f"Unterminated string literal starting at position {self.pos - len(str_literal)}")

    def make_specialchar(self):
        id_str = self.current_char
        self.advance()

        while self.current_char is not None and self.current_char in SPECIALCHAR:
            id_str += self.current_char
            self.advance()

        return Token(TT_SPECIALCHAR, id_str)

class NumberNode:
    def __init__(self, tok):
        self.tok = tok

    def __repr__(self):
        return f'{self.tok}'

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
    
class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'


class ParseResult:
    def __init__(self):
        self.error = None
        self.node = None

    def register(self, res):
        if isinstance(res, ParseResult):
            if res.error:
                self.error = res.error
            return res.node

        return res

    def success(self, node):
        self.node = node
        return self

    def failure(self, error):
        self.error = error
        return self

# Parser
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]
        return self.current_tok

    def parse(self):
        res = self.expr()
        if not res.error and self.current_tok.type != TT_EOF:
            return res.failure(InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '+', '-', '*' or '/'"
            ))
        return res

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_ADD, TT_SUB):
            res.register(self.advance())
            factor = res.register(self.factor())
            if res.error:
                return res
            return res.success(UnaryOpNode(tok, factor))

        elif tok.type in (TT_INT, TT_FLOAT):
            res.register(self.advance())
            return res.success(NumberNode(tok))

        elif tok.type == TT_LPAREN:
            res.register(self.advance())
            expr = res.register(self.expr())
            if res.error:
                return res
            if self.current_tok.type == TT_RPAREN:
                res.register(self.advance())
                return res.success(expr)
            else:
                return res.failure(InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        return res.failure(InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int or float"
        ))

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_DIV))

    def expr(self):
        return self.bin_op(self.term, (TT_ADD, TT_SUB))

    def bin_op(self, func, ops):
        res = ParseResult()
        left = res.register(func())
        if res.error:
            return res

        while self.current_tok.type in ops:
            op_tok = self.current_tok
            res.register(self.advance())
            right = res.register(func())
            if res.error:
                return res
            left = BinOpNode(left, op_tok, right)

        return res.success(left)

###############################
# RUN
###############################

def run(filename):
    try:
        _, file_extension = os.path.splitext(filename)

        if file_extension != '.supp':
            return [], f"Error: Unsupported file type '{file_extension}'"

        with open(filename, 'r') as file:
            text = file.read()

        lexer = Lexer(text)
        tokens, error = lexer.make_tokens()

        if error:
            return None, error

        parser = Parser(tokens)
        ast = parser.parse()

        return ast.node, ast.error

    except FileNotFoundError:
        return [], f"Error: File '{filename}' not found"


def run_from_code(code):
    try:
        lexer = Lexer(code)
        tokens, error = lexer.make_tokens()

        if error:
            return None, error

        parser = Parser(tokens)
        ast = parser.parse()

        return ast.node, ast.error

    except Exception as e:
        return [], f"An error occurred: {str(e)}"
