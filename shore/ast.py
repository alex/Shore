from shore.builtins import Integer
from shore.context import Context
from shore.utils import CompileError


def bind_to_module(obj, module):
    if hasattr(obj, "bind_to_module"):
        obj.bind_to_module(module)
    elif isinstance(obj, (tuple, list)):
        for obj in obj:
            bind_to_module(obj, module)

class BaseNode(object):
    attrs = []
    needs_bind_to_module = []
    
    def __init__(self,  *args):
        for attr, value in zip(self.attrs, args):
            setattr(self, attr, value)
    
    def __repr__(self):
        if not self.attrs:
            return "(%r)" % type(self).__name__
        return "(%r, %s)" % (
            type(self).__name__, ", ".join(repr(getattr(self, attr)) for attr in self.attrs)
        )
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (not self.attrs or
                all(getattr(self, attr) == getattr(other, attr) for attr in self.attrs))
        return (other[0] == type(self).__name__ and (not self.attrs or
            all(getattr(self, attr) == other[i+1] for i, attr in enumerate(self.attrs))))
    
    def bind_to_module(self, module):
        for attr in self.needs_bind_to_module:
            bind_to_module(getattr(self, attr), module)


class NodeList(object):
    def __init__(self, nodes):
        self.nodes = nodes
    
    def __repr__(self):
        return "[%s]" % ", ".join(map(repr, self.nodes))
    
    def __eq__(self, other):
        if isinstance(other, NodeList):
            return self.nodes == other.nodes
        return self.nodes == other
    
    def bind_to_module(self, module):
        for node in self.nodes:
            node.bind_to_module(module)
    
    def verify(self, context):
        for node in self.nodes:
            node.verify(context)

class NoneNode(BaseNode):
    attrs = []
    needs_bind_to_module = []

class BooleanNode(BaseNode):
    attrs = ["value"]
    needs_bind_to_module = []

class StringNode(BaseNode):
    attrs = ["value"]
    needs_bind_to_module = []

class IntegerNode(BaseNode):
    attrs = ["value"]
    needs_bind_to_module = []
    
    def verify(self, context):
        pass
    
    def type(self, context):
        return Integer

class FloatNode(BaseNode):
    attrs = ["value"]
    needs_bind_to_module = []

class BinOpNode(BaseNode):
    attrs = ["left", "right", "op"]
    needs_bind_to_module = ["left", "right"]
    
    def get_func(self, context):
        method_names = {
            "*": "__mul__",
            "/": "__div__",
            "%": "__mod__",
            "+": "__add__",
            "-": "__sub__",
            "&": "__and__",
            "|": "__or__",
            "^": "__xor__",
        }
        
        left_type, right_type = self.left.type(context), self.right.type(context)
        method = method_names[self.op]
        reverse_method = "__r%s__" % method.split("__")[1]
        if method in left_type.functions:
            if left_type.functions[method].arguments[1][1] is right_type:
                return left_type.functions[method]
        if reverse_method in right_type.functions:
            if right_type.functions[reverse_method].arguments[1][1] is left_type:
                return right_type.functions[method]
        raise CompileError("Can't do %s on %s, %s" % (self.op, left_type, right_type))
    
    def verify(self, context):
        self.left.verify(context)
        self.right.verify(context)
        self.get_func(context)
    
    def type(self, context):
        return self.get_func(context).return_type

class CompNode(BaseNode):
    attrs = ["left", "right", "op"]
    needs_bind_to_module = ["left", "right"]
    
    def verify(self, context):
        method_names = {
            "==": "__eq__",
            "!=": "__ne__",
            ">": "__gt__",
            "<": "__lt__",
            ">=": "__ge__",
            "<=": "__le__",
        }
        self.left.verify(context)
        self.right.verify(context)
        
        left_type, right_type = self.left.type(context), self.right.type(context)
        method = method_names[self.op]
        if method not in left_type.functions:
            raise CompileError("Can't do %s on %s" % (self.op, self.left_type))
        if left_type.functions[method].arguments[1][1] is not right_type:
            raise CompileError("Can't do %s on types %s, %s" % (self.op,
                left_type, right_type))

class ContainsNode(BaseNode):
    attrs = ["obj", "seq"]
    needs_bind_to_module = ["obj", "seq"]

class UnaryOpNode(BaseNode):
    attrs = ["value", "op"]
    needs_bind_to_module = ["value"]

class NameNode(BaseNode):
    attrs = ["name"]
    
    def bind_to_module(self, module):
        if self.name in module.classes:
            self.value = module.classes[self.name]
        elif self.name in module.functions:
            self.value = module.functions[self.name]
    
    def verify(self, context):
        if not hasattr(self, "value") and self.name not in context:
            raise CompileError("%s not declared" % self.name)
    
    def type(self, context):
        return context[self.name]

class DeclarationNode(BaseNode):
    attrs = ["type", "name", "value"]
    needs_bind_to_module = ["type", "value"]

class SubscriptNode(BaseNode):
    attrs = ["value", "index"]
    needs_bind_to_module = ["value", "index"]

class TemplateNode(BaseNode):
    attrs = ["type", "parameters"]
    needs_bind_to_module = ["type", "parameters"]

class AssignmentNode(BaseNode):
    attrs = ["name", "value"]
    needs_bind_to_module = ["value"]

class ItemAssignmentNode(BaseNode):
    attrs = ["lhs", "index", "value"]
    needs_bind_to_module = ["lhs", "index", "value"]

class AttrAssignmentNode(BaseNode):
    attrs = ["lhs", "attr", "value"]
    needs_bind_to_module = ["lhs", "attr", "value"]

class IfNode(BaseNode):
    attrs = ["conditions", "else_body"]
    needs_bind_to_module = ["conditions", "else_body"]
    
    def verify(self, context):
        for condition, body in self.conditions:
            condition.verify(context)
            context.push()
            body.verify(context)
            context.pop()
        if self.else_body is not None:
            context.push()
            self.else_body.verify(context)
            context.pop()


class WhileNode(BaseNode):
    attrs = ["condition", "body"]
    needs_bind_to_module = ["condtion", "body"]

class ForNode(BaseNode):
    attrs = ["name", "value", "body"]
    needs_bind_to_module = ["value", "body"]

class FunctionNode(BaseNode):
    attrs = ["name", "templates", "return_type", "arguments", "body"]
    needs_bind_to_module = ["templates", "arguments", "body"]
    
    def bind_to_module(self, module):
        super(FunctionNode, self).bind_to_module(module)
        self.return_type = module.classes[self.return_type.name] if self.return_type is not None else None
    
    def verify(self, context=None):
        if context is None:
            context = Context(self.return_type)
        context.push()
        for name, type, default in self.arguments:
            if not hasattr(type, "value"):
                raise CompileError("Argument %s for %s's type doesn't exist." % (name, self.name))
            context[name] = type.value
        
        self.body.verify(context)

class ReturnNode(BaseNode):
    attrs = ["value"]
    needs_bind_to_module = ["value"]
    
    def verify(self, context):
        self.value.verify(context)
        if context.return_type is not self.value.type(context):
            raise CompileError("Return type does not match returned type.")

class ClassNode(BaseNode):
    attrs = ["name", "templates", "superclasses", "body"]
    needs_bind_to_module = ["superclasses", "body"]

class PassNode(BaseNode):
    attrs = []

class CallNode(BaseNode):
    attrs = ["function", "arguments"]
    needs_bind_to_module = ["arguments"]
    
    def bind_to_module(self, module):
        super(CallNode, self).bind_to_module(module)
        self.function = module.functions[self.function.name]
    
    def verify(self, context):
        # TODO: Doens't handle named, or default arguments
        args = self.function.arguments
        if len(args) != len(self.arguments):
            raise CompileError("Argument count mismatch, %s expected, received %s" %
                (len(args), len(self.arguments)))
        for expected_arg, provided_arg in zip(args, self.arguments):
            expected_type = expected_arg[1].value if hasattr(expected_arg[1], "value") else expected_arg[1]
            if expected_type is not provided_arg[1].type(context):
                raise CompileError("Argument type mismatch, %s expected, recieved %s" %
                    (expected_type, provided_arg[1].type(context)))
    
    def type(self, context):
        return self.function.return_type

class AttributeNode(BaseNode):
    attrs = ["value", "attribute"]
    needs_bind_to_module = ["value"]

class BreakNode(BaseNode):
    attrs = []
