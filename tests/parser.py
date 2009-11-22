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

if __name__ == "__main__":
    unittest.main()
