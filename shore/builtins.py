"""
Definitions for various builtins.
"""


RECURSIVE_TYPE_CONSTANT = "self"


class Function(object):
    def __init__(self, return_type, arguments):
        self.return_type = return_type
        self.arguments = arguments
    
    def bind_to_module(self, module):
        pass
    
    def verify(self):
        pass

class BuiltinTypeMetaclass(type):
    def __new__(cls, name, bases, attrs):
        functions = dict([(n, attr) for n, attr in attrs.iteritems()
            if isinstance(attr, Function)])
        for attr in functions:
            attrs.pop(attr)
        new_cls = super(BuiltinTypeMetaclass, cls).__new__(cls, name, bases, attrs)
        new_cls.functions = {}
        for name, function in functions.iteritems():
            if function.return_type == RECURSIVE_TYPE_CONSTANT:
                function.return_type = new_cls
            for i, argument in enumerate(function.arguments):
                if argument[1] == RECURSIVE_TYPE_CONSTANT:
                    function.arguments[i] = (argument[0], new_cls, argument[2])
            new_cls.functions[name] = function
        return new_cls


class Builtin(object):
    __metaclass__ = BuiltinTypeMetaclass

    @classmethod
    def bind_to_module(cls, module):
        pass
    
    @classmethod
    def verify(cls):
        pass


class Boolean(Builtin):
    pass

class Integer(Builtin):
    __eq__ = Function(Boolean, [(None, "self", None), (None, "self", None)])
    __add__ = Function("self", [(None, "self", None), (None, "self", None)])
    __sub__ = Function("self", [(None, "self", None), (None, "self", None)])

class String(Builtin):
    pass

Print = Function(String, [(None, Integer, None)])
