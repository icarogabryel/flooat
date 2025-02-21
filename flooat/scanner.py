import re


IGNORED_CHARS = [' ', '\t', '\n']
END_OF_FILE = '\0'
END_OF_COMMENT = ['\n', END_OF_FILE]
KEY_WORDS_DICT = {
    'main': 'main',
    'comp': 'comp',
    'in': 'in',
    'out': 'out',
    'bit': 'bit',
    'not': 'not',
    'nor': 'nor',
    'and': 'and',
    'nand': 'nand',
    'xor': 'xor',
    'or': 'or',
}
SYMBOLS_DICT = {
    ';': 'semicolon',
    '(': 'l_paren',
    ')': 'r_paren',
    '{': 'l_brace',
    '}': 'r_brace',
    '=': 'assign'
}


class LexicalError(Exception):
    def __init__(self, line_number, message):
        self.message = message
        self.line_number = line_number

    def __str__(self):
        return f"Lexical Error at line {self.line_number}: {self.message}"


class Token():
    def __init__(self, label, lexeme):
        self.label = label
        self.lexeme = lexeme

    def __str__(self):
        return f'({self.label}, "{self.lexeme}")'

    def __repr__(self):
        return self.__str__()


class Scanner():
    def __init__(self, code: str):
        self.code = code + END_OF_FILE
        self.line_number = 1
        self.index = 0

    def advance(self):
        if self.get_char() == '\n':
            self.line_number += 1

        self.index += 1

    def get_char(self) -> str:
        return self.code[self.index]

    def is_eof(self) -> bool:
        return True if self.get_char() == END_OF_FILE else False

    def skip_ignored(self):
        while not self.is_eof():  # While don't reach the end of the string
            while self.get_char() in IGNORED_CHARS:  # Skip ignored characters
                self.advance()

            if self.get_char() == '/':  # Skip line comments
                if self.code[self.index + 1] == '/':  # Prevent self.index + 1 out of range
                    while self.get_char() not in END_OF_COMMENT:
                        self.advance()
            else:  # If it's not an ignored character, break the loop
                break

    def read(self):  # Read the next lexeme
        lexeme = ''

        while not self.is_eof():  # While don't reach the end of the string
            if (char := self.get_char()) in SYMBOLS_DICT: # If it's a symbol, stop reading and return the lexeme
                return lexeme
            elif char in IGNORED_CHARS: # If it's an ignored character, stop reading and return the lexeme
                return lexeme
            else:  # If it's not an ignored character or a symbol, keep reading
                lexeme += char
                self.advance()

        return lexeme

    def get_token(self):
        self.skip_ignored()
        token = None

        if self.is_eof():
            token = Token('EOF', END_OF_FILE)

        elif (char := self.get_char()) in SYMBOLS_DICT:
            token = Token(SYMBOLS_DICT[char], char)
            self.advance()

        elif re.match(r'[a-zA-Z_\d]', char):  # Check if the character can be the start of a word
            lexeme = self.read()

            if lexeme in KEY_WORDS_DICT:
                token = Token(KEY_WORDS_DICT[lexeme], lexeme)

            elif re.match(r'^[a-zA-Z]\w*$', lexeme):  # Check if the lexeme is a valid identifier
                token = Token('id', lexeme)

            elif lexeme in ['0', '1']:  # Check if the lexeme is a valid binary number  #todo change to accept more than one bit
                token = Token('bin', lexeme)

            else:
                raise LexicalError(self.line_number, f'Invalid lexeme: {lexeme}')

        else:
            raise LexicalError(self.line_number, f"Invalid character: {char}")

        return token

    def get_token_stream(self):
        while not self.is_eof():
            yield self.get_token()
