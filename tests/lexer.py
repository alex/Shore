#!/usr/bin/env python

import unittest
from itertools import izip_longest

from shore.lexer import Lexer


def pad(s, length=20):
    s = str(s)
    return s + " " * (max(0, length - len(s)))

class LexerTest(unittest.TestCase):
    def assert_lexes(self, string, tokens):
        result = list(Lexer(string).parse())
        diffs = ["%s\t\t%s\t\t%s" % (pad(expected), pad(seen, 35), expected == seen) for expected, seen in izip_longest(tokens, result)]
        error_message = "\n".join([""] + diffs)
        self.assertEqual(result, tokens, error_message)
    
    def test_simple(self):
        self.assert_lexes("""a = 3""", [
            ("NAME", "a"),
            ("EQUAL", "="),
            ("NUMBER", "3"),
            ("NEWLINE", "\n"),
        ])
        
        self.assert_lexes("""a = 3\nb = a""", [
            ("NAME", "a"),
            ("EQUAL", "="),
            ("NUMBER", "3"),
            ("NEWLINE", "\n"),
            ("NAME", "b"),
            ("EQUAL", "="),
            ("NAME", "a"),
            ("NEWLINE", "\n"),
        ])
        
        self.assert_lexes("""a = 3\nb = a\nc="a+3"\nd = c""", [
            ("NAME", "a"),
            ("EQUAL", "="),
            ("NUMBER", "3"),
            ("NEWLINE", "\n"),
            ("NAME", "b"),
            ("EQUAL", "="),
            ("NAME", "a"),
            ("NEWLINE", "\n"),
            ("NAME", "c"),
            ("EQUAL", "="),
            ("STRING", "a+3"),
            ("NEWLINE", "\n"),
            ("NAME", "d"),
            ("EQUAL", "="),
            ("NAME", "c"),
            ("NEWLINE", "\n"),
        ])
        
        self.assert_lexes("""abc2 = 342""", [
            ("NAME", "abc2"),
            ("EQUAL", "="),
            ("NUMBER", "342"),
            ("NEWLINE", "\n"),
        ])
        
        self.assert_lexes("""a = "\\\""\nb = a""", [
            ("NAME", "a"),
            ("EQUAL", "="),
            ("STRING", '"'),
            ("NEWLINE", "\n"),
            ("NAME", "b"),
            ("EQUAL", "="),
            ("NAME", "a"),
            ("NEWLINE", "\n"),
        ])
        
        self.assert_lexes("""True or False""", [
            ("TRUE", "True"),
            ("OR", "or"),
            ("FALSE", "False"),
            ("NEWLINE", "\n"),
        ])
        
        self.assert_lexes("""a is not None""", [
            ("NAME", "a"),
            ("ISNOT", "is not"),
            ("NONE", "None"),
            ("NEWLINE", "\n"),
        ])
    
    def test_math(self):
        self.assert_lexes("""a = 3\nb = a*2 - a/9""", [
            ("NAME", "a"),
            ("EQUAL", "="),
            ("NUMBER", "3"),
            ("NEWLINE", "\n"),
            ("NAME", "b"),
            ("EQUAL", "="),
            ("NAME", "a"),
            ("STAR", "*"),
            ("NUMBER", "2"),
            ("MINUS", "-"),
            ("NAME", "a"),
            ("SLASH", "/"),
            ("NUMBER", "9"),
            ("NEWLINE", "\n"),
        ])
        
        self.assert_lexes("""int a = 5\nint b = 5 * a""", [
            ("NAME", "int"),
            ("NAME", "a"),
            ("EQUAL", "="),
            ("NUMBER", "5"),
            ("NEWLINE", "\n"),
            ("NAME", "int"),
            ("NAME", "b"),
            ("EQUAL", "="),
            ("NUMBER", "5"),
            ("STAR", "*"),
            ("NAME", "a"),
            ("NEWLINE", "\n"),
        ])
        
        self.assert_lexes("""a ** b""", [
            ("NAME", "a"),
            ("STARSTAR", "**"),
            ("NAME", "b"),
            ("NEWLINE", "\n"),
        ])
        
        self.assert_lexes("""dict<str, int>""", [
            ("NAME", "dict"),
            ("LESS", "<"),
            ("NAME", "str"),
            ("COMMA", ","),
            ("NAME", "int"),
            ("GREATER", ">"),
            ("NEWLINE", "\n"),
        ])
    
    def test_indent(self):
        self.assert_lexes("""for i in range(5):\n    print(i)""", [
            ("FOR", "for"),
            ("NAME", "i"),
            ("IN", "in"),
            ("NAME", "range"),
            ("LPAR", "("),
            ("NUMBER", "5"),
            ("RPAR", ")"),
            ("COLON", ":"),
            ("NEWLINE", "\n"),
            ("INDENT", ""),
            ("NAME", "print"),
            ("LPAR", "("),
            ("NAME", "i"),
            ("RPAR", ")"),
            ("NEWLINE", "\n"),
            ("DEDENT", ""),
        ])
        
        self.assert_lexes("""for i in range(5):\n    print(i)\n    print(i)\nprint(3)""", [
            ("FOR", "for"),
            ("NAME", "i"),
            ("IN", "in"),
            ("NAME", "range"),
            ("LPAR", "("),
            ("NUMBER", "5"),
            ("RPAR", ")"),
            ("COLON", ":"),
            ("NEWLINE", "\n"),
            ("INDENT", ""),
            ("NAME", "print"),
            ("LPAR", "("),
            ("NAME", "i"),
            ("RPAR", ")"),
            ("NEWLINE", "\n"),
            ("NAME", "print"),
            ("LPAR", "("),
            ("NAME", "i"),
            ("RPAR", ")"),
            ("NEWLINE", "\n"),
            ("DEDENT", ""),
            ("NAME", "print"),
            ("LPAR", "("),
            ("NUMBER", "3"),
            ("RPAR", ")"),
            ("NEWLINE", "\n"),
        ])


if __name__ == "__main__":
    unittest.main()
