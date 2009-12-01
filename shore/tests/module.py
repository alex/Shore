#!/usr/bin/env python

import unittest

from shore.main import Shore


class ModuleTest(unittest.TestCase):
    def generate_code(self, source):
        return Shore("\n".join(source)).generate_code()
    
    def test_simple(self):
        source = [
            "int def factorial(int n):",
            "    if n == 0:",
            "        return 1",
            "    return factorial(n-1) + factorial(n-2)",
            "",
            "def main():",
            "    print(factorial(5))",
            "    print(factorial(13))",
        ]
        m = self.generate_code(source)
        print m


if __name__ == "__main__":
    unittest.main()
