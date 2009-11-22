class NodeList(object):
    def __init__(self, nodes):
        self.nodes = nodes
    
    def __repr__(self):
        return "[%s]" % ", ".join(map(repr, self.nodes))
    
    def __eq__(self, other):
        if isinstance(other, NodeList):
            return self.nodes == other.nodes
        return self.nodes == other


class BooleanNode(object):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return "(%r, %r)" % (type(self).__name__, self.value)
    
    def __eq__(self, other):
        if isinstance(other, BooleanNode):
            return self.value == other.value
        return other[0] == type(self).__name__ and other[1] == self.value


class NoneNode(object):
    def __repr__(self):
        return "(%r)" % type(self).__name__
    
    def __eq__(self, other):
        if isinstance(other, NoneNode):
            return True
        return other[0] == type(self).__name__


class StringNode(object):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return "(%r, %r)" % (type(self).__name__, self.value)
    
    def __eq__(self, other):
        if isinstance(other, StringNode):
            return self.value == other.value
        return other[0] == type(self).__name__ and other[1] == self.value


class IntegerNode(object):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return "(%r, %r)" % (type(self).__name__, self.value)

    def __eq__(self, other):
        if isinstance(other, IntegerNode):
            return self.value == other.value
        return other[0] == type(self).__name__ and other[1] == self.value


class FloatNode(object):
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return "(%r, %r)" % (type(self).__name__, self.value)

    def __eq__(self, other):
        if isinstance(other, FloatNode):
            return self.value == other.value
        return other[0] == type(self).__name__ and other[1] == self.value


class BinOpNode(object):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op
    
    def __repr__(self):
        return "(%r, %r, %r, %r)" % (type(self).__name__, self.left, self.right, self.op)

    def __eq__(self, other):
        if isinstance(other, BinOpNode):
            return self.left == other.left and self.right == other.right and self.op == other.op
        return (other[0] == type(self).__name__ and other[1] == self.left and
            other[2] == self.right and other[3] == self.op)


class CompNode(object):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op
    
    def __repr__(self):
        return "(%r, %r, %r, %r)" % (type(self).__name__, self.left, self.right, self.op)
    
    def __eq__(self, other):
        if isinstance(other, CompNode):
            return self.left == other.left and self.right == other.right and self.op == other.op
        return (other[0] == type(self).__name__ and other[1] == self.left and
            other[2] == self.right and other[3] == self.op)


class ContainsNode(object):
    def __init__(self, obj, seq):
        self.obj = obj
        self.seq = seq
    
    def __repr__(self):
        return "(%r, %r, %r)" % (type(self).__name__, self.obj, self.seq)
    
    def __eq__(self, other):
        if isinstance(other, ContainsNode):
            return self.obj == other.obj and self.seq == other.seq
        return (other[0] == type(self).__name__ and other[1] == self.obj and
            other[2] == self.seq)


class UnaryOpNode(object):
    def __init__(self, value, op):
        self.value = value
        self.op = op
    
    def __repr__(self):
        return "(%r, %r, %r)" % (type(self).__name__, self.value, self.op)
    
    def __eq__(self, other):
        if isinstance(other, UnaryOpNode):
            return self.value == other.value and self.op == other.op
        return other[0] == type(self).__name__ and other[1] == self.value and other[2] == self.op


class NameNode(object):
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return "(%r, %r)" % (type(self).__name__, self.name)
    
    def __eq__(self, other):
        if isinstance(other, NameNode):
            return self.name == other.name
        return other[0] == type(self).__name__ and other[1] == self.name


class DeclarationNode(object):
    def __init__(self, type, name, value):
        self.type = type
        self.name = name
        self.value = value
    
    def __repr__(self):
        return "(%r, %r, %r, %r)" % (type(self).__name__, self.type, self.name, self.value)
    
    def __eq__(self, other):
        if isinstance(other, DeclarationNode):
            return (self.type == other.type and self.name == other.name and
                self.value == other.value)
        return (other[0] == type(self).__name__ and other[1] == self.type and
            other[2] == self.name and other[3] == self.value)
