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

if __name__ == "__main__":
    unittest.main()
