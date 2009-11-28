#!/usr/bin/env python

import unittest
from itertools import izip_longest

from shore.lexer import Lexer


def pad(s, length=20):
    s = str(s)
    return s + " " * (max(0, length - len(s)))

class LexerTest(unittest.TestCase):
    def assert_lexes(self, string, tokens):
        result = list(Lexer("\n".join(string)).parse())
        diffs = ["%s\t\t%s\t\t%s" % (pad(expected), pad(seen, 35), expected == seen) for expected, seen in izip_longest(tokens, result)]
        error_message = "\n".join([""] + diffs)
        self.assertEqual(result, tokens, "\n".join([""] + string+ ["", ""]) + error_message)
    
    def test_simple(self):
        data = [
            "a = 3",
        ]
        self.assert_lexes(data, [
            ("NAME", "a"),
            ("EQUAL", "="),
            ("NUMBER", "3"),
            ("NEWLINE", "\n"),
        ])
        
        data = [
            "a = 3",
            "b = a",
        ]
        self.assert_lexes(data, [
            ("NAME", "a"),
            ("EQUAL", "="),
            ("NUMBER", "3"),
            ("NEWLINE", "\n"),
            ("NAME", "b"),
            ("EQUAL", "="),
            ("NAME", "a"),
            ("NEWLINE", "\n"),
        ])
        
        data = [
            "a = 3",
            "b = a",
            'c = "a+3"',
            "d = c",
        ]
        self.assert_lexes(data, [
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
        
        data = [
            "abc2 = 342",
        ]
        self.assert_lexes(data, [
            ("NAME", "abc2"),
            ("EQUAL", "="),
            ("NUMBER", "342"),
            ("NEWLINE", "\n"),
        ])
        
        data = [
            'a = "\\\""',
            "b = a",
        ]
        self.assert_lexes(data, [
            ("NAME", "a"),
            ("EQUAL", "="),
            ("STRING", '"'),
            ("NEWLINE", "\n"),
            ("NAME", "b"),
            ("EQUAL", "="),
            ("NAME", "a"),
            ("NEWLINE", "\n"),
        ])
        
        data = [
            "True or False",
        ]
        self.assert_lexes(data, [
            ("TRUE", "True"),
            ("OR", "or"),
            ("FALSE", "False"),
            ("NEWLINE", "\n"),
        ])
        
        data = [
            "a is not None",
        ]
        self.assert_lexes(data, [
            ("NAME", "a"),
            ("ISNOT", "is not"),
            ("NONE", "None"),
            ("NEWLINE", "\n"),
        ])
    
    def test_math(self):
        data = [
            "a = 3",
            "b = a*2 - a/9",
        ]
        self.assert_lexes(data, [
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
        
        data = [
            "int a = 5",
            "int b = 5 * a",
        ]
        self.assert_lexes(data, [
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
        
        data = [
            "a ** b",
        ]
        self.assert_lexes(data, [
            ("NAME", "a"),
            ("STARSTAR", "**"),
            ("NAME", "b"),
            ("NEWLINE", "\n"),
        ])
        
        data = [
            "dict<str, int>",
        ]
        self.assert_lexes(data, [
            ("NAME", "dict"),
            ("LESS", "<"),
            ("NAME", "str"),
            ("COMMA", ","),
            ("NAME", "int"),
            ("GREATER", ">"),
            ("NEWLINE", "\n"),
        ])
    
    def test_indent(self):
        data = [
            "for i in range(5):",
            "    print(i)",
        ]
        self.assert_lexes(data, [
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
        
        data = [
            "if not a:",
            "    a = l",
            "else:",
            "    a[0] = 2",
        ]
        self.assert_lexes(data, [
            ("IF", "if"),
            ("NOT", "not"),
            ("NAME", "a"),
            ("COLON", ":"),
            ("NEWLINE", "\n"),
            ("INDENT", ""),
            ("NAME", "a"),
            ("EQUAL", "="),
            ("NAME", "l"),
            ("NEWLINE", "\n"),
            ("DEDENT", ""),
            ("ELSE", "else"),
            ("COLON", ":"),
            ("NEWLINE", "\n"),
            ("INDENT", ""),
            ("NAME", "a"),
            ("LSQB", "["),
            ("NUMBER", "0"),
            ("RSQB", "]"),
            ("EQUAL", "="),
            ("NUMBER", "2"),
            ("NEWLINE", "\n"),
            ("DEDENT", ""),
        ])
        
        data = [
            "for i in range(5):",
            "    print(i)",
            "    print(i)",
            "print(3)",
        ]
        self.assert_lexes(data, [
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
