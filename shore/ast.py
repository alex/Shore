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

class FloatNode(BaseNode):
    attrs = ["value"]
    needs_bind_to_module = []

class BinOpNode(BaseNode):
    attrs = ["left", "right", "op"]
    needs_bind_to_module = ["left", "right"]

class CompNode(BaseNode):
    attrs = ["left", "right", "op"]
    needs_bind_to_module = ["left", "right"]

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

class WhileNode(BaseNode):
    attrs = ["condition", "body"]
    needs_bind_to_module = ["condtion", "body"]

class ForNode(BaseNode):
    attrs = ["name", "value", "body"]
    needs_bind_to_module = ["value", "body"]

class FunctionNode(BaseNode):
    attrs = ["name", "templates", "return_type", "arguments", "body"]
    needs_bind_to_module = ["templates", "return_type", "arguments", "body"]
    
    def verify(self, context=None):
        if context is None:
            context = {}
        if self.return_type is not None and not hasattr(self.return_type, "value"):
            raise CompileError("Return type for %s doesn't exist." % self.name)
        for name, type, default in self.arguments:
            if not hasattr(type, "value"):
                raise CompileError("Argument %s for %s's type doesn't exist." % (name, self.name))

class ReturnNode(BaseNode):
    attrs = ["value"]
    needs_bind_to_module = ["value"]

class ClassNode(BaseNode):
    attrs = ["name", "templates", "superclasses", "body"]
    needs_bind_to_module = ["superclasses", "body"]

class PassNode(BaseNode):
    attrs = []

class CallNode(BaseNode):
    attrs = ["function", "arguments"]
    needs_bind_to_module = ["function", "arguments"]

class AttributeNode(BaseNode):
    attrs = ["value", "attribute"]
    needs_bind_to_module = ["value"]

class BreakNode(BaseNode):
    attrs = []
