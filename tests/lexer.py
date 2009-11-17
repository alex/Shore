#!/usr/bin/env python

import unittest

from shore.lexer import Lexer


def pad(s, length=15):
    return s + " " * (max(0, length - len(s)))

class LexerTest(unittest.TestCase):
    def assert_lexes(self, string, tokens):
        result = list(Lexer(string).parse())
        diffs = ["%s\t\t%s\t\t\t%s" % (pad(str(expected)), seen, expected == seen) for expected, seen in zip(tokens, result)]
        error_message = "\n".join([""] + diffs)
        self.assertEqual(result, tokens, error_message)
    
    def test_simple(self):
        self.assert_lexes("""a = 3""", [
            ("name", "a"),
            ("equal", "="),
            ("number", "3")
        ])
        
        self.assert_lexes("""a = 3\nb = a""", [
            ("name", "a"),
            ("equal", "="),
            ("number", "3"),
            ("newline", "\n"),
            ("name", "b"),
            ("equal", "="),
            ("name", "a"),
        ])
        
        self.assert_lexes("""a = 3\nb = a\nc="a+3"\nd = c""", [
            ("name", "a"),
            ("equal", "="),
            ("number", "3"),
            ("newline", "\n"),
            ("name", "b"),
            ("equal", "="),
            ("name", "a"),
            ("newline", "\n"),
            ("name", "c"),
            ("equal", "="),
            ("string", "a+3"),
            ("newline", "\n"),
            ("name", "d"),
            ("equal", "="),
            ("name", "c"),
        ])
        
        self.assert_lexes("""abc2 = 342""", [
            ("name", "abc2"),
            ("equal", "="),
            ("number", "342"),
        ])
        
        self.assert_lexes("""a = "\\\""\nb = a""", [
            ("name", "a"),
            ("equal", "="),
            ("string", '"'),
            ("newline", "\n"),
            ("name", "b"),
            ("equal", "="),
            ("name", "a")
        ])
    
    def test_math(self):
        self.assert_lexes("""a = 3\nb = a*2 - a/9""", [
            ("name", "a"),
            ("equal", "="),
            ("number", "3"),
            ("newline", "\n"),
            ("name", "b"),
            ("equal", "="),
            ("name", "a"),
            ("star", "*"),
            ("number", "2"),
            ("minus", "-"),
            ("name", "a"),
            ("slash", "/"),
            ("number", "9"),
        ])
        
        self.assert_lexes("""int a = 5\nint b = 5 * a""", [
            ("name", "int"),
            ("name", "a"),
            ("equal", "="),
            ("number", "5"),
            ("newline", "\n"),
            ("name", "int"),
            ("name", "b"),
            ("equal", "="),
            ("number", "5"),
            ("star", "*"),
            ("name", "a"),
        ])
    
    def test_indent(self):
        self.assert_lexes("""for i in range(5):\n    print(i)\n    print(i)\nprint(3)""", [
            ("for", "for"),
            ("name", "i"),
            ("in", "in"),
            ("name", "range"),
            ("lpar", "("),
            ("number", "5"),
            ("rpar", ")"),
            ("colon", ":"),
            ("newline", "\n"),
            ("indent", ""),
            ("name", "print"),
            ("lpar", "("),
            ("name", "i"),
            ("rpar", ")"),
            ("newline", "\n"),
            ("name", "print"),
            ("lpar", "("),
            ("name", "i"),
            ("rpar", ")"),
            ("newline", "\n"),
            ("dedent", ""),
            ("name", "print"),
            ("lpar", "("),
            ("number", "3"),
            ("rpar", ")"),
        ])


if __name__ == "__main__":
    unittest.main()
