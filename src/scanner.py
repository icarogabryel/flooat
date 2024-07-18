from io import TextIOWrapper
from shared import IGNORED_CHARS, SYMBOLS


class Token:
    def __init__(self, label, lexeme) -> None:
        self.label = label
        self.lexeme = lexeme

    def __str__(self) -> str:
        return f'{self.label}: {self.lexeme}'


class Scanner:
    def __init__(self, code: TextIOWrapper) -> None:
        self.code = code # The code to be analyzed
        self.currentLine = self.getLine() # Contains the current line analyzed
        self.currentLineCounter = 1 # Indicates the current line number analyzed. is used in error messages
        self.index = 0 # Point to the current char analyzed in the code

    def getLine(self):
        line = self.code.readline()
        
        if line == '':
            return '\0'
        else:
            return line

    def advance(self): # Increment the index to the next char
        if self.index < len(self.currentLine) - 1: # If the index is not the last char in the line, increment it
            self.index += 1
        
        else: # Else update the current line, increment line counter and reset the index to the beginning of the new line
                self.currentLine = self.getLine()
                self.currentLineCounter += 1
                self.index = 0

    def getCurrentChar(self):
        return self.currentLine[self.index]
    
    def isEof(self):
        return True if self.getCurrentChar() == '\0' else False
    
    def passIgnoredChars(self):
        while self.getCurrentChar() in IGNORED_CHARS:
            self.advance()

        if self.getCurrentChar() == '#':
            while self.getCurrentChar() != '\n':
                self.advance()

            self.advance()
        
        if self.getCurrentChar() in IGNORED_CHARS or self.getCurrentChar() == '#':
            self.passIgnoredChars()
    
    def getNextToken(self):
        self.passIgnoredChars()

        if self.isEof():
            return Token('EOF', '')
           
        if self.getCurrentChar() in SYMBOLS:
            token = Token('SYMBOL', self.getCurrentChar())
            self.advance()

            return token
