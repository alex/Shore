#!/usr/bin/env python

import os
import subprocess
import sys

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

class Main(object):
    def __init__(self, args):
        self.args = args
    
    def main(self):
        f = self.args[1]
        code = Shore(open(f).read()).generate_code()
        open("ir.cpp", "w").write(code)
        pwd = os.path.dirname(os.path.abspath(__file__))
        loc = os.path.join(pwd, "runtime")
        ret = subprocess.call(["g++", "ir.cpp", os.path.join(pwd, "runtime", "gc.cpp"), "-I%s" % loc])
        if ret == 0:
            os.remove("ir.cpp")

if __name__ == "__main__":
    Main(sys.argv).main()
