#!/usr/bin/env python

import unittest

from shore.parser import Parser


class ParserTest(unittest.TestCase):
    def assert_parses(self, text):
        return Parser(text).parse()
    
    def test_simple(self):
        self.assert_parses("""3 + 4""")
        

if __name__ == "__main__":
    unittest.main()
