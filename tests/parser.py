#!/usr/bin/env python

import unittest

from shore.parser import Parser


class ParserTest(unittest.TestCase):
    def assert_parses(self, text, expected):
        ast = Parser("\n".join(text)).parse()
        self.assertEqual(expected, ast)
    
    def test_simple(self):
        data = [
            "3 + 4",
        ]
        self.assert_parses(data, [
            ("BinOpNode", ("IntegerNode", "3"), ("IntegerNode", "4"), "+"),
        ])
        
        data = [
            "True or False",
        ]
        self.assert_parses(data, [
            ("BinOpNode", ("BooleanNode", True), ("BooleanNode", False), "or"),
        ])
        
        data = [
            "True or False and True",
        ]
        self.assert_parses(data, [
            ("BinOpNode", ("BinOpNode", ("BooleanNode", True), ("BooleanNode", False), "or"), ("BooleanNode", True), "and"),
        ])
        
        data = [
            "int a = 3",
            "float c = a + 4.5",
        ]
        self.assert_parses(data, [
            ("DeclarationNode", ("NameNode", "int"), "a", ("IntegerNode", "3")),
            ("DeclarationNode", ("NameNode", "float"), "c", ("BinOpNode", ("NameNode", "a"), ("FloatNode", "4.5"), "+")),
        ])
        
        data = [
            'bool b = "a" in seq',
        ]
        self.assert_parses(data, [
            ("DeclarationNode", ("NameNode", "bool"), "b", ("ContainsNode", ("StringNode", "a"), ("NameNode", "seq")))
        ])
        
        data = [
            "b not in seq",
        ]
        self.assert_parses(data, [
            ("UnaryOpNode", ("ContainsNode", ("NameNode", "b"), ("NameNode", "seq")), "not")
        ])
        
        data = [
            "val is None",
        ]
        self.assert_parses(data, [
            ("CompNode", ("NameNode", "val"), ("NoneNode",), "is"),
        ])
        
        data = [
            "val is not None",
        ]
        self.assert_parses(data, [
            ("UnaryOpNode", ("CompNode", ("NameNode", "val"), ("NoneNode",), "is"), "not"),
        ])
        
        data = [
            "val[2]",
        ]
        self.assert_parses(data, [
            ("SubscriptNode", ("NameNode", "val"), ("IntegerNode", "2")),
        ])
        
        data = [
            ".4 / 4.",
        ]
        self.assert_parses(data, [
            ("BinOpNode", ("FloatNode", "0.4"), ("FloatNode", "4.0"), "/"),
        ])
        
        data = [
            "str c = None",
        ]
        self.assert_parses(data, [
            ("DeclarationNode", ("NameNode", "str"), "c", ("NoneNode",))
        ])
        
        data = [
            "a ** b ** c",
        ]
        self.assert_parses(data, [
            ("BinOpNode", ("NameNode", "a"), ("BinOpNode", ("NameNode", "b"), ("NameNode", "c"), "**"), "**"),
        ])
        
        data = [
            "a < 2",
        ]
        self.assert_parses(data, [
            ("CompNode", ("NameNode", "a"), ("IntegerNode", "2"), "<"),
        ])
        
        data = [
            "list{int}",
        ]
        self.assert_parses(data, [
            ("TemplateNode", ("NameNode", "list"), [("NameNode", "int")]),
        ])
        
        data = [
            "dict{str, int}",
        ]
        self.assert_parses(data, [
            ("TemplateNode", ("NameNode", "dict"), [("NameNode", "str"), ("NameNode", "int")]),
        ])
        
        data = [
            "list{str} c = None",
        ]
        self.assert_parses(data, [
            ("DeclarationNode", ("TemplateNode", ("NameNode", "list"), [("NameNode", "str")]), "c", ("NoneNode",)),
        ])
        
        data = [
            "a = 2",
        ]
        self.assert_parses(data, [
            ("AssignmentNode", "a", ("IntegerNode", "2")),
        ])
        
        data = [
            "a[3] = 2",
        ]
        self.assert_parses(data, [
            ("ItemAssignmentNode", ("NameNode", "a"), ("IntegerNode", "3"), ("IntegerNode", "2")),
        ])
        
        data = [
            "a.b = 2",
        ]
        self.assert_parses(data, [
            ("AttrAssignmentNode", ("NameNode", "a"), "b", ("IntegerNode", "2")),
        ])
        
        data = [
            "if a:",
            "    a[3] = 2",
        ]
        self.assert_parses(data, [
            ("IfNode", [(("NameNode", "a"), [
                ("ItemAssignmentNode", ("NameNode", "a"), ("IntegerNode", "3"), ("IntegerNode", "2")),
            ])], None)
        ])
        
        data = [
            "if not a:",
            "    a = l",
            "else:",
            "    a[0] = 2",
        ]
        self.assert_parses(data, [
            ("IfNode", [(("UnaryOpNode", ("NameNode", "a"), "not"), [
                ("AssignmentNode", "a", ("NameNode", "l")),
            ])], [
                ("ItemAssignmentNode", ("NameNode", "a"), ("IntegerNode", "0"), ("IntegerNode", "2"))
            ]),
        ])
        
        data = [
            "if not a:",
            "    a = l",
            "elif a == 2:",
            "    a = 3",
            "elif a == 3:",
            "    a = 4",
        ]
        self.assert_parses(data, [
            ("IfNode", [
                (("UnaryOpNode", ("NameNode", "a"), "not"), [
                    ("AssignmentNode", "a", ("NameNode", "l")),
                ]),
                (("CompNode", ("NameNode", "a"), ("IntegerNode", "2"), "=="), [
                    ("AssignmentNode", "a", ("IntegerNode", "3")),
                ]),
                (("CompNode", ("NameNode", "a"), ("IntegerNode", "3"), "=="), [
                    ("AssignmentNode", "a", ("IntegerNode", "4")),
                ]),
            ], None)
        ])

        data = [
            "if not a:",
            "    a = l",
            "elif a == 3:",
            "    a = 4",
            "else:",
            "    a = 3",
        ]
        self.assert_parses(data, [
            ("IfNode", [
                (("UnaryOpNode", ("NameNode", "a"), "not"), [
                    ("AssignmentNode", "a", ("NameNode", "l")),
                ]),
                (("CompNode", ("NameNode", "a"), ("IntegerNode", "3"), "=="), [
                    ("AssignmentNode", "a", ("IntegerNode", "4")),
                ]),
            ], [
                ("AssignmentNode", "a", ("IntegerNode", "3")),
            ])
        ])
        
        data = [
            "while a < 10:",
            "    a = a + 1",
        ]
        self.assert_parses(data, [
            ("WhileNode", ("CompNode", ("NameNode", "a"), ("IntegerNode", "10"), "<"), [
                ("AssignmentNode", "a", ("BinOpNode", ("NameNode", "a"), ("IntegerNode", "1"), "+")),
            ])
        ])
        
        data = [
            "for x in y:",
            "    x + 1",
        ]
        self.assert_parses(data, [
            ("ForNode", "x", ("NameNode", "y"), [
                ("BinOpNode", ("NameNode", "x"), ("IntegerNode", "1"), "+"),
            ])
        ])
        
        data = [
            "T def{T} first(iterable{T} items):",
            "    return items[0]",
        ]
        self.assert_parses(data, [
            ("FunctionNode", "first", [("NameNode", "T")], ("NameNode", "T"), [
                ("items", ("TemplateNode", ("NameNode", "iterable"), [("NameNode", "T")]), None)
            ], [
                ("ReturnNode", ("SubscriptNode", ("NameNode", "items"), ("IntegerNode", "0"))),
            ])
        ])
        
        data = [
            "str def hello(str name):",
            '    return "hello " + name',
        ]
        self.assert_parses(data, [
            ("FunctionNode", "hello", [], ("NameNode", "str"), [
                ("name", ("NameNode", "str"), None),
            ], [
                ("ReturnNode", ("BinOpNode", ("StringNode", "hello "), ("NameNode", "name"), "+"))
            ])
        ])
        
        data = [
            "def{T} mutate(iterable{T} items):",
            "    items[0] = items[1]",
        ]
        self.assert_parses(data, [
            ("FunctionNode", "mutate", [("NameNode", "T")], None, [
                ("items", ("TemplateNode", ("NameNode", "iterable"), [("NameNode", "T")]), None),
            ], [
                ("ItemAssignmentNode", ("NameNode", "items"), ("IntegerNode", "0"), ("SubscriptNode", ("NameNode", "items"), ("IntegerNode", "1"))),
            ]),
        ])
        
        data = [
            "def mutate(list{str} items):",
            '    items[0] = "lol"'
        ]
        self.assert_parses(data, [
            ("FunctionNode", "mutate", [], None, [
                ("items", ("TemplateNode", ("NameNode", "list"), [("NameNode", "str")]), None),
            ], [
                ("ItemAssignmentNode", ("NameNode", "items"), ("IntegerNode", "0"), ("StringNode", "lol")),
            ]),
        ])


if __name__ == "__main__":
    unittest.main()
