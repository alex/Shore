#!/usr/bin/env python

import unittest

from shore.lexer import Lexer


class LexerTest(unittest.TestCase):
    def assert_lexes(self, string, tokens):
        result = list(Lexer(string).parse())
        diffs = ["%s\t\t\t\t%s" % (expected, seen) for expected, seen in zip(tokens, result)]
        error_message = "\n".join([None] + diffs)
        self.assertEqual(result, tokens, error_message)
    
    def test_simple(self):
        self.assert_lexes("""a = 3""", [
            ("name", "a"),
            ("=", "="),
            ("number", "3")
        ])
        
        self.assert_lexes("""a = 3\nb = a""", [
            ("name", "a"),
            ("=", "="),
            ("number", "3"),
            ("newline", "\n"),
            ("name", "b"),
            ("=", "="),
            ("name", "a"),
        ])
        
        self.assert_lexes("""a = 3\nb = a\nc="a+3"\nd = c""", [
            ("name", "a"),
            ("=", "="),
            ("number", "3"),
            ("newline", "\n"),
            ("name", "b"),
            ("=", "="),
            ("name", "a"),
            ("newline", "\n"),
            ("name", "c"),
            ("=", "="),
            ("string", "a+3"),
            ("newline", "\n"),
            ("name", "d"),
            ("=", "="),
            ("name", "c"),
        ])
        
        self.assert_lexes("""abc2 = 342""", [
            ("name", "abc2"),
            ("=", "="),
            ("number", "342"),
        ])
        
        self.assert_lexes("""a = "\\\""\nb = a""", [
            ("name", "a"),
            ("=", "="),
            ("string", '"'),
            ("newline", "\n"),
            ("name", "b"),
            ("=", "="),
            ("name", "a")
        ])
    
    def test_math(self):
        self.assert_lexes("""a = 3\nb = a*2 - a/9""", [
            ("name", "a"),
            ("=", "="),
            ("number", "3"),
            ("newline", "\n"),
            ("name", "b"),
            ("=", "="),
            ("name", "a"),
            ("*", "*"),
            ("number", "2"),
            ("-", "-"),
            ("name", "a"),
            ("/", "/"),
            ("number", "9"),
        ])
        
        self.assert_lexes("""int a = 5\nint b = 5 * a""", [
            ("name", "int"),
            ("name", "a"),
            ("=", "="),
            ("number", "5"),
            ("newline", "\n"),
            ("name", "int"),
            ("name", "b"),
            ("=", "="),
            ("number", "5"),
            ("*", "*"),
            ("name", "a"),
        ])
    
    def test_indent(self):
        self.assert_lexes("""for i in range(5):\n    print(i)\n    print(i)\nprint(3)""", [
            ("name", "for"),
            ("name", "i"),
            ("name", "in"),
            ("name", "range"),
            ("(", "("),
            ("number", "5"),
            (")", ")"),
            (":", ":"),
            ("newline", "\n"),
            ("indent", ""),
            ("name", "print"),
            ("(", "("),
            ("name", "i"),
            (")", ")"),
            ("newline", "\n"),
            ("name", "print"),
            ("(", "("),
            ("name", "i"),
            (")", ")"),
            ("newline", "\n"),
            ("dedent", ""),
            ("name", "print"),
            ("(", "("),
            ("number", "3"),
            (")", ")"),
        ])


if __name__ == "__main__":
    unittest.main()
