#!/usr/bin/env python

import os
import subprocess
import sys

import argparse

from shore.builtins import Integer, Boolean, String, List, Print, Range
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
            "str": String,
            "list": List
        }, {
            "print": Print,
            "range": Range,
        })
        m.from_ast(self.parse())
        return m

    def generate_code(self):
        return self.to_module().generate_code()

class Main(object):
    def main(self):
        parser = argparse.ArgumentParser(description="The shore compiler.")
        parser.add_argument("file", type=argparse.FileType("r"), help="The file to compile.")
        parser.add_argument("-o", default="a.out", help="The out files name.")
        parser.add_argument("-S", action="store_true", default=False,
            help="Output the assembley, instead of the executable.")
        parser.add_argument("--dont-remove", action="store_true", default=False,
            help="Don't delete the IR (C++) after compiling.")
        parser.add_argument("--parse", action="store_true", default=False,
            help="Only parse the file to an AST (and print the AST to stdout).")

        args = parser.parse_args()
        shore = Shore(args.file.read())
        if args.parse:
            print shore.parse()
            return

        code = shore.generate_code()
        open("ir.cpp", "w").write(code)
        pwd = os.path.dirname(os.path.abspath(__file__))
        loc = os.path.join(pwd, "runtime")
        cmdline_args = [
            "g++",
            "-g",
            "-Wall",
            "ir.cpp",
            os.path.join(loc, "gc.cpp"),
            os.path.join(loc, "int.cpp"),
            os.path.join(loc, "str.cpp"),
            os.path.join(loc, "bool.cpp"),
            os.path.join(loc, "slice.cpp"),
            "-I%s" % loc,
        ]
        if args.S:
            cmdline_args.append("-S")
        cmdline_args.append("-o%s" % args.o)
        ret = subprocess.call(cmdline_args)
        if not args.dont_remove:
            os.remove("ir.cpp")

if __name__ == "__main__":
    Main().main()
