#!/usr/bin/env python

import unittest

from shore.parser import Parser


class ParserTest(unittest.TestCase):
    def assert_parses(self, text, expected):
        ast = Parser(text).parse()
        self.assertEqual(expected, ast)
    
    def test_simple(self):
        self.assert_parses("""3 + 4""", [
            ("BinOpNode", ("IntegerNode", "3"), ("IntegerNode", "4"), "+"),
        ])
        self.assert_parses("""True or False""", [
            ("BinOpNode", ("BooleanNode", True), ("BooleanNode", False), "or"),
        ])
        self.assert_parses("""int a = 3\nfloat c = a + 4.5""", [
            ("DeclarationNode", ("NameNode", "int"), "a", ("IntegerNode", "3")),
            ("DeclarationNode", ("NameNode", "float"), "c", ("BinOpNode", ("NameNode", "a"), ("FloatNode", "4.5"), "+")),
        ])
        self.assert_parses("""bool b = "a" in seq""", [
            ("DeclarationNode", ("NameNode", "bool"), "b", ("ContainsNode", ("StringNode", "a"), ("NameNode", "seq")))
        ])
        self.assert_parses("""b not in seq""", [
            ("UnaryOpNode", ("ContainsNode", ("NameNode", "b"), ("NameNode", "seq")), "not")
        ])
        self.assert_parses("""val is None""", [
            ("CompNode", ("NameNode", "val"), ("NoneNode",), "is"),
        ])
        self.assert_parses("""val is not None""", [
            ("UnaryOpNode", ("CompNode", ("NameNode", "val"), ("NoneNode",), "is"), "not"),
        ])
        self.assert_parses("""val[2]""", [
            ("SubscriptNode", ("NameNode", "val"), ("IntegerNode", "2")),
        ])

if __name__ == "__main__":
    unittest.main()
