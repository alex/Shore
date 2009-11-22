class BaseNode(object):
    attrs = []
    
    def __repr__(self):
        return "(%r, %s)" % (
            type(self).__name__, ", ".join(repr(getattr(self, attr)) for attr in self.attrs)
        )
    
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return all(getattr(self, attr) == getattr(other, attr) for attr in self.attrs)
        return (other[0] == type(self).__name__ and
            all(getattr(self, attr) == other[i+1] for i, attr in enumerate(self.attrs)))

class NodeList(object):
    def __init__(self, nodes):
        self.nodes = nodes
    
    def __repr__(self):
        return "[%s]" % ", ".join(map(repr, self.nodes))
    
    def __eq__(self, other):
        if isinstance(other, NodeList):
            return self.nodes == other.nodes
        return self.nodes == other


class BooleanNode(BaseNode):
    attrs = ["value"]
    
    def __init__(self, value):
        self.value = value


class NoneNode(object):
    def __repr__(self):
        return "(%r)" % type(self).__name__
    
    def __eq__(self, other):
        if isinstance(other, NoneNode):
            return True
        return other[0] == type(self).__name__


class StringNode(BaseNode):
    attrs = ["value"]
    
    def __init__(self, value):
        self.value = value


class IntegerNode(BaseNode):
    attrs = ["value"]

    def __init__(self, value):
        self.value = value
    

class FloatNode(BaseNode):
    attrs = ["value"]
    
    def __init__(self, value):
        self.value = value
    

class BinOpNode(BaseNode):
    attrs = ["left", "right", "op"]
    
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op


class CompNode(BaseNode):
    attrs = ["left", "right", "op"]
    
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

class ContainsNode(BaseNode):
    attrs = ["obj", "seq"]
    
    def __init__(self, obj, seq):
        self.obj = obj
        self.seq = seq

class UnaryOpNode(BaseNode):
    attrs = ["value", "op"]
    
    def __init__(self, value, op):
        self.value = value
        self.op = op
    

class NameNode(BaseNode):
    attrs = ["name"]
    
    def __init__(self, name):
        self.name = name


class DeclarationNode(BaseNode):
    attrs = ["type", "name", "value"]
    
    def __init__(self, type, name, value):
        self.type = type
        self.name = name
        self.value = value


class SubscriptNode(BaseNode):
    attrs = ["value", "index"]
    
    def __init__(self, value, index):
        self.value = value
        self.index = index
