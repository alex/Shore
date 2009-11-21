from collections import deque
from copy import copy

from ply import yacc

from shore.utils import PLYCompatLexer


class Parser(object):
    def __init__(self, text):
        self.text = text
        self.parser = yacc.yacc(module=self)
    
    def parse(self):
        return self.parser.parse(lexer=PLYCompatLexer(self.text))
