from shore.builtins import Integer, Boolean, Print
from shore.lexer import Lexer
from shore.module import Module
from shore.parser import Parser
from shore.utils import PLYCompatLexer


class Shore(object):
    def __init__(self, source):
        self.source = source
    
    def tokenize(self):
        return Lexer(self.source).tokenize()
    
    def parse(self):
        return Parser(PLYCompatLexer(self.tokenize())).parse()
    
    def to_module(self):
        m = Module("__main__")
        m.add_builtins({
            "bool": Boolean,
            "int": Integer,
        }, {
            "print": Print
        })
        m.from_ast(self.parse())
        return m
    
    def generate_code(self):
        return self.to_module().generate_code()
