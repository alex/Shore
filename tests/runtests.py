import unittest

from shore.parser import Parser
from shore.tests.lexer import LexerTest
from shore.tests.parser import ParserTest


if __name__ == "__main__":
    # This is here to spool up the parser and make sure the parsetab file is
    # regenerated if necessary.
    Parser("1").parse()
    unittest.main()
