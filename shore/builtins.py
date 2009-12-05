"""
Definitions for various builtins.
"""
from shore.utils import CompileError


RECURSIVE_TYPE_CONSTANT = "self"

class Signature(object):
    def __init__(self, return_type, arguments):
        self.return_type = return_type
        self.arguments = arguments
    
    def bind(self, substitutions):
        if self.return_type in substitutions:
            self.return_type = substitutions[self.return_type]
        for i, argument in enumerate(self.arguments):
            if argument[1] in substitutions:
                self.arguments[i] = (argument[0], substitutions[argument[1]], argument[2])
    
    def matches(self, arguments):
        # TODO: Default args.
        if len(self.arguments) != len(arguments):
            return False
        for expected, received in zip(self.arguments, arguments):
            if expected[1] is not received[1]:
                return False
        return True
    

class Function(object):
    def __init__(self, signatures, name=None):
        self.signatures = signatures
        self.name = name
    
    def matches(self, arguments):
        return any(signature.matches(arguments) for signature in self.signatures)

    def get_matching_signature(self, arguments):
        for signature in self.signatures:
            if signature.matches(arguments):
                return signature
        raise CompileError("No matching signature.")
    
    def bind_to_module(self, module):
        pass
    
    def verify(self):
        pass
    
    def get_frame_class(self):
        return []
    
    def generate_code(self):
        return []

class BuiltinTypeMetaclass(type):
    def __new__(cls, name, bases, attrs):
        functions = dict([(n, attr) for n, attr in attrs.iteritems()
            if isinstance(attr, Function)])
        for attr in functions:
            attrs.pop(attr)
        new_cls = super(BuiltinTypeMetaclass, cls).__new__(cls, name, bases, attrs)
        new_cls.functions = {}
        for name, function in functions.iteritems():
            for signature in function.signatures:
                signature.bind({RECURSIVE_TYPE_CONSTANT: new_cls})
            new_cls.functions[name] = function
        return new_cls


class Builtin(object):
    __metaclass__ = BuiltinTypeMetaclass

    @staticmethod
    def bind_to_module(module):
        pass
    
    @staticmethod
    def verify():
        pass
    
    @staticmethod
    def generate_code():
        return []
    
    @classmethod
    def compatible(cls, type):
        # TODO: subclasses
        return type is None or type is cls


class Template(Builtin):
    templated_over = []
    
    def __init__(self, *types):
        self.templates = dict(zip(self.templated_over, types))
        for function in self.functions.values():
            for signature in function.signatures:
                signature.bind(self.templates)

class List(Template):
    templated_over = ["T"]
    
    


class Boolean(Builtin):
    pass

class Integer(Builtin):
    class_name = "shore::builtin__int"
    
    __eq__ = Function([
        Signature(Boolean, [(None, "self", None), (None, "self", None)])
    ])
    __add__ = Function([
        Signature("self", [(None, "self", None), (None, "self", None)])
    ])
    __sub__ = Function([
        Signature("self", [(None, "self", None), (None, "self", None)])
    ])
    __mul__ = Function([
        Signature("self", [(None, "self", None), (None, "self", None)])
    ])


class String(Builtin):
    class_name = "shore::builtin__str"
    
    __mul__ = Function([
        Signature("self", [(None, "self", None), (None, Integer, None)]),
    ])


Print = Function([
    Signature(None, [(None, Integer, None)]),
    Signature(None, [(None, String, None)]),
], name="builtin__print")

Range = Function([
    Signature(List(Integer), [(None, Integer, None)]),
    Signature(List(Integer), [(None, Integer, None), (None, Integer, None)]),
    Signature(List(Integer), [(None, Integer, None), (None, Integer, None), (None, Integer, None)]),
], name="builtin__range")
