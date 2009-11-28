class BaseNode(object):
    attrs = []
    
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

class NodeList(object):
    def __init__(self, nodes):
        self.nodes = nodes
    
    def __repr__(self):
        return "[%s]" % ", ".join(map(repr, self.nodes))
    
    def __eq__(self, other):
        if isinstance(other, NodeList):
            return self.nodes == other.nodes
        return self.nodes == other

class NoneNode(BaseNode):
    attrs = []

class BooleanNode(BaseNode):
    attrs = ["value"]

class StringNode(BaseNode):
    attrs = ["value"]

class IntegerNode(BaseNode):
    attrs = ["value"]

class FloatNode(BaseNode):
    attrs = ["value"]

class BinOpNode(BaseNode):
    attrs = ["left", "right", "op"]

class CompNode(BaseNode):
    attrs = ["left", "right", "op"]

class ContainsNode(BaseNode):
    attrs = ["obj", "seq"]

class UnaryOpNode(BaseNode):
    attrs = ["value", "op"]

class NameNode(BaseNode):
    attrs = ["name"]

class DeclarationNode(BaseNode):
    attrs = ["type", "name", "value"]

class SubscriptNode(BaseNode):
    attrs = ["value", "index"]

class TemplateNode(BaseNode):
    attrs = ["type", "parameters"]

class AssignmentNode(BaseNode):
    attrs = ["name", "value"]

class ItemAssignmentNode(BaseNode):
    attrs = ["lhs", "index", "value"]

class AttrAssignmentNode(BaseNode):
    attrs = ["lhs", "attr", "value"]

class IfNode(BaseNode):
    attrs = ["conditions", "else_body"]

class WhileNode(BaseNode):
    attrs = ["condition", "body"]

class ForNode(BaseNode):
    attrs = ["name", "value", "body"]

class FunctionNode(BaseNode):
    attrs = ["name", "templates", "return_type", "arguments", "body"]

class ReturnNode(BaseNode):
    attrs = ["value"]

class ClassNode(BaseNode):
    attrs = ["name", "templates", "superclasses", "body"]

class PassNode(BaseNode):
    attrs = []
