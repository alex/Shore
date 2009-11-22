class NodeList(object):
    def __init__(self, nodes):
        self.nodes = nodes


class BooleanNode(object):
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):
        if isinstance(other, BooleanNode):
            return self.value == other.value
        return other[0] == type(self).__name__ and other[1] == self.value


class NoneNode(object):
    pass


class StringNode(object):
    def __init__(self, value):
        self.value = value


class IntegerNode(object):
    def __init__(self, value):
        self.value = value
    
    def __eq__(self, other):
        if isinstance(other, IntegerNode):
            return self.value == other.value
        return other[0] == type(self).__name__ and other[1] == self.value


class FloatNode(object):
    def __init__(self, value):
        self.value = value


class BinOpNode(object):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

    def __eq__(self, other):
        if isinstance(other, BinOpNode):
            return self.left == other.left and self.right == other.right and self.op == other.op
        return (other[0] == type(self).__name__ and other[1] == self.left and
            other[2] == self.right and other[3] == self.op)


class CompOpNode(object):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op


class ContainsNode(object):
    def __init__(self, seq, obj):
        self.seq = seq
        self.obj = obj


class UnaryOpNode(object):
    def __init__(self, value, op):
        self.value = value
        self.op = op


class NameNode(object):
    def __init__(self, name):
        self.name = name
