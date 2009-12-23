from shore.builtins import Integer, String, Boolean, Slice
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
    
    def get_locals(self):
        variables = {}
        for node in self.nodes:
            if hasattr(node, "get_locals"):
                variables.update(node.get_locals())
        return variables
    
    def generate_code(self):
        code = []
        for node in self.nodes:
            co = node.generate_code()
            if isinstance(co, basestring):
                code.append("%s;" % co)
            else:
                code.extend(co)
        return code

class NoneNode(BaseNode):
    attrs = []
    needs_bind_to_module = []
    
    def verify(self, context):
        pass
    
    def type(self, context):
        return None
    
    def generate_code(self):
        return "NULL"

class BooleanNode(BaseNode):
    attrs = ["value"]
    needs_bind_to_module = []
    
    def verify(self, context):
        pass
    
    def type(self, context):
        return Boolean
    
    def generate_code(self):
        return "shore::builtin__bool::new_instance(%s)" % str(self.value).lower()

class StringNode(BaseNode):
    attrs = ["value"]
    needs_bind_to_module = []
    
    def type(self, context):
        return String
    
    def generate_code(self):
        return "shore::builtin__str::new_instance(\"%s\")" % self.value

class IntegerNode(BaseNode):
    attrs = ["value"]
    needs_bind_to_module = []
    
    def verify(self, context):
        pass
    
    def type(self, context):
        return Integer
    
    def generate_code(self):
        return "shore::builtin__int::new_instance(%sLL)" % self.value

class FloatNode(BaseNode):
    attrs = ["value"]
    needs_bind_to_module = []

class BinOpNode(BaseNode):
    attrs = ["left", "right", "op"]
    needs_bind_to_module = ["left", "right"]

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
    reverse_method_names = {
        "*": "__rmul__",
        "/": "__rdiv__",
        "%": "__rmod__",
        "+": "__radd__",
        "-": "__rsub__",
    }
    
    def get_func(self, context, signature=False):
        left_type, right_type = self.left.type(context), self.right.type(context)
        method = self.method_names[self.op]
        reverse_method = self.reverse_method_names[self.op]
        if method in left_type.functions:
            if left_type.functions[method].matches([(None, left_type), (None, right_type)]):
                if signature:
                    return left_type.functions[method].get_matching_signature([(None, left_type), (None, right_type)]), False
                else:
                    return left_type.functions[method], False
        if reverse_method in right_type.functions:
            if right_type.functions[reverse_method].arguments[1][1] is left_type:
                if signature:
                    return right_type.functins[reverse].get_matching_signature([(None, right_type), (None, left_type)]), True
                else:
                    return right_type.functions[reverse_method], True
        raise CompileError("Can't do %s on %s, %s" % (self.op, left_type, right_type))
    
    def verify(self, context):
        self.left.verify(context)
        self.right.verify(context)
        self.reverse = self.get_func(context)[1]
    
    def type(self, context):
        return self.get_func(context, signature=True)[0].return_type
    
    def generate_code(self):
        left = self.left.generate_code()
        right = self.right.generate_code()
        if self.reverse:
            return "(%s)->%s(%s)" % (right, self.reverse_method_namse[self.op], left)
        return "(%s)->%s(%s)" % (left, self.method_names[self.op], right)

class CompNode(BaseNode):
    attrs = ["left", "right", "op"]
    needs_bind_to_module = ["left", "right"]

    method_names = {
        "==": "__eq__",
        "!=": "__ne__",
        ">": "__gt__",
        "<": "__lt__",
        ">=": "__ge__",
        "<=": "__le__",
    }
    
    def verify(self, context):
        self.left.verify(context)
        self.right.verify(context)
        
        left_type, right_type = self.left.type(context), self.right.type(context)
        method = self.method_names[self.op]
        if method not in left_type.functions:
            raise CompileError("Can't do %s on %s" % (self.op, left_type))
        left_type.functions[method].get_matching_signature([(None, left_type), (None, right_type)])
    
    def type(self, context):
        return self.left.type(context).functions[self.method_names[self.op]].get_matching_signature([(None, self.left.type(context)), (None, self.right.type(context))]).return_type
    
    def generate_code(self):
        left = self.left.generate_code()
        right = self.right.generate_code()
        return "(%s)->%s(%s)" % (left, self.method_names[self.op], right)

class BooleanCompNode(BaseNode):
    attrs = ["left", "right", "op"]
    needs_bind_to_module = ["left", "right"]
    
    def verify(self, context):
        self.left.verify(context)
        self.right.verify(context)
    
    def type(self, context):
        return Boolean
    
    def generate_code(self):
        if self.op == "and":
            op = "&&"
        elif self.op == "or":
            op == "||"
        else:
            raise CompileError
        return "shore::builtin__bool::new_instance((%s)->__bool__()->value %s (%s)->__bool__()->value)" % (self.left.generate_code(), op, self.right.generate_code())

class ContainsNode(BaseNode):
    attrs = ["obj", "seq"]
    needs_bind_to_module = ["obj", "seq"]

class UnaryOpNode(BaseNode):
    attrs = ["value", "op"]
    needs_bind_to_module = ["value"]
    
    def verify(self, context):
        self.value.verify(context)
        if self.op == "not":
            return
        # TODO: Handle other cases
        raise Exception
    
    def generate_code(self):
        if self.op == "not":
            code = self.value.generate_code()
            return "shore::builtin__bool::new_instance(!(%s)->value)" % code
        # TODO: Handle other cases
        raise Exception

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
        if not hasattr(self, "value"):
            self.bound_type = self.type(context)
    
    def type(self, context):
        return context[self.name]
    
    def as_function(self, context):
        return self.value
    
    def generate_code(self):
        if hasattr(self, "value"):
            return [self.value.class_name]
        return "frame.%s" % self.name

class DeclarationNode(BaseNode):
    attrs = ["type", "name", "value"]
    needs_bind_to_module = ["type", "value"]
    
    def verify(self, context):
        context[self.name] = self.type.value
        self.value.verify(context)
        if not self.type.value.compatible(self.value.type(context)):
            raise CompileError("%s RHS doesn't match type." % (self.name))
    
    def get_locals(self):
        return {self.name: self.type.value}
    
    def generate_code(self):
        return ["frame.%s = %s;" % (self.name, self.value.generate_code())]

class SubscriptNode(BaseNode):
    attrs = ["value", "index"]
    needs_bind_to_module = ["value", "index"]
    
    def type(self, context):
        type = self.value.type(context)
        return type.functions["__getitem__"].get_matching_signature([
            (None, type),
            (None, self.index.type(context)),
        ]).return_type
    
    def verify(self, context):
        if "__getitem__" not in  self.value.type(context).functions:
            raise CompileError("Can't subscript %s" % self.value.type(context))
        if not self.value.type(context).functions["__getitem__"].matches([
            (None, self.value.type(context)),
            (None, self.index.type(context)),
        ]):
            raise CompileError("Can't do %s[%s]" % (
                self.value.type(context), self.index.type(context)
            ))
    
    def generate_code(self):
        return "%s->__getitem__(%s)" % (self.value.generate_code(), self.index.generate_code())

class TemplateNode(BaseNode):
    attrs = ["type", "parameters"]
    needs_bind_to_module = ["type", "parameters"]
    
    def bind_to_module(self, module):
        super(TemplateNode, self).bind_to_module(module)
        self.value = self.type.value(*[param.value for param in self.parameters])

class AssignmentNode(BaseNode):
    attrs = ["name", "value"]
    needs_bind_to_module = ["value"]
    
    def verify(self, context):
        self.value.verify(context)
        if self.name not in context:
            raise CompileError("%s isn't declared." % self.name)
        if not context[self.name].compatible(self.value.type(context)):
            raise CompileError("%s RHS doesn't match type." % (self.name))
    
    def generate_code(self):
        return "frame.%s = %s" % (self.name, self.value.generate_code())

class ItemAssignmentNode(BaseNode):
    attrs = ["lhs", "index", "value"]
    needs_bind_to_module = ["lhs", "index", "value"]
    
    def verify(self, context):
        self.lhs.verify(context)
        self.index.verify(context)
        self.value.verify(context)
        
        if not self.lhs.type(context).functions["__setitem__"].matches([
            (None, self.lhs.type(context)),
            (None, self.index.type(context)),
            (None, self.value.type(context)),
        ]):
            raise CompileError("Can't do %s[%s] = %s" % (
                self.lhs.type(context), self.index.type(context), self.value.type(context)
            ))
    
    def generate_code(self):
        return "%s->__setitem__(%s, %s)" % (
            self.lhs.generate_code(), self.index.generate_code(), self.value.generate_code()
        )

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
    
    def get_locals(self):
        locs = {}
        for _, body in self.conditions:
            locs.update(body.get_locals())
        if self.else_body is not None:
            locs.update(self.else_body.get_locals())
        return locs
    
    def generate_code(self):
        code = []
        conditions = iter(self.conditions)
        condition, body = conditions.next()
        code.append("if ((%s)->__bool__()->value) {" % condition.generate_code())
        code.extend(body.generate_code())
        code.append("}")
        for condition, body in conditions:
            code.append("else if ((%s)->__bool__()->value) {" % condition.generate_code())
            code.extend(body.generate_code())
            code.append("}")
        if self.else_body is not None:
            code.append("else {")
            code.extend(self.else_body.generate_code())
            code.append("}")
        return code


class WhileNode(BaseNode):
    attrs = ["condition", "body"]
    needs_bind_to_module = ["condition", "body"]
    
    def verify(self, context):
        self.condition.verify(context)
        self.body.verify(context)
    
    def generate_code(self):
        code = ["while ((%s)->value) {" % self.condition.generate_code()]
        code.extend(self.body.generate_code())
        code.append("}")
        return code
    
    def get_locals(self):
        return self.body.get_locals()

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
    
    def matches(self, arguments):
        # TODO: Default args.
        if len(self.arguments) != len(arguments):
            return False
        for expected, received in zip(self.arguments, arguments):
            if expected[1].value is not received[1]:
                return False
        return True

    def returns(self, arguments):
        return self.return_type
    
    def get_locals(self):
        variables = dict([(name, type.value) for name, type, default in self.arguments])
        variables.update(self.body.get_locals())
        if self.return_type is not None:
            variables["_return_"] = self.return_type
        return variables
    
    def get_frame_class(self):
        variables = self.get_locals()
        code = [
            "class %s__frame : public shore::Frame {" % self.name,
            "public:",
        ]
        for name, type in variables.iteritems():
            code.append("%(type)s* %(name)s;" % {"name": name, "type": type.class_name})
        code.append("shore::GCSet __get_sub_objects() {")
        code.append("shore::GCSet s;")
        for name in variables:
            code.append("s.insert(this->%s);" % (name))
        code.append("return s;")
        code.append("}")
        code.append("};")
        return code
    
    def get_declaration(self):
        return ["%(return_type)s %(name)s(%(parameters)s);" % {
            "return_type": self.return_type.class_name+"*" if self.return_type is not None else "void",
            "name": self.name if self.name != "main" else "app_main",
            "parameters": ", ".join("%s* %s" % (type.value.class_name, name) for name, type, default in self.arguments),
        }]
    
    def generate_code(self):
        code = [
            "%(return_type)s %(name)s(%(parameters)s) {" % {
                "return_type": self.return_type.class_name+"*" if self.return_type is not None else "void",
                "name": self.name if self.name != "main" else "app_main",
                "parameters": ", ".join(["%s* %s" % (type.value.class_name, name) for name, type, default in self.arguments]),
            },
        ]
        code.append("%s__frame frame;" % self.name)
        code.append("shore::State::frames.push_back(&frame);")

        for name in self.get_locals():
            code.append("frame.%s = NULL;" % name)

        for name, _, _ in self.arguments:
            code.append("frame.%s = %s;" % (name, name))
        
        code.extend(self.body.generate_code())
        
        if self.return_type is None:
            code.append("shore::State::frames.pop_back();")
            code.append("shore::GC::collect();")
        code.append("}")
        return code

class ReturnNode(BaseNode):
    attrs = ["value"]
    needs_bind_to_module = ["value"]
    
    def verify(self, context):
        self.value.verify(context)
        if context.return_type is not self.value.type(context):
            raise CompileError("Return type does not match returned type.")
    
    def generate_code(self):
        code = []
        code.append("frame._return_ = %s;" % self.value.generate_code())
        code.append("shore::GC::collect();")
        code.append("shore::State::frames.pop_back();")
        code.append("return frame._return_;")
        return code

class ClassNode(BaseNode):
    attrs = ["name", "templates", "superclasses", "body"]
    needs_bind_to_module = ["superclasses", "body"]

class PassNode(BaseNode):
    attrs = []

class CallNode(BaseNode):
    attrs = ["function", "arguments"]
    needs_bind_to_module = ["function", "arguments"]
    
    def verify(self, context):
        self.function = self.function.as_function(context)
        if not self.function.matches([(name, node.type(context)) for name, node in self.arguments]):
            raise CompileError("Argument mismatch")
    
    def type(self, context):
        return self.function.returns([(name, node.type(context)) for name, node in self.arguments])
    
    def generate_code(self):
        # TODO: named args
        if hasattr(self.function, "class_name"):
            func = "%s::new_instance" % self.function.class_name
        else:
            func = self.function.generate_code()
        return "%s(%s)" % (func, ", ".join(arg.generate_code() for name, arg in self.arguments))

class AttributeNode(BaseNode):
    attrs = ["value", "attribute"]
    needs_bind_to_module = ["value"]

class BreakNode(BaseNode):
    attrs = []
    
    def verify(self, context):
        pass
    
    def generate_code(self):
        return "break"

class SliceNode(BaseNode):
    attrs = ["start", "stop", "step"]
    
    def type(self, context):
        return Slice
    
    def generate_code(self):
        start = self.start.generate_code() if self.start is not None else "NULL"
        stop = self.stop.generate_code() if self.stop is not None else "NULL"
        step = self.step.generate_code() if self.step is not None else "NULL"
        return "shore::builtin__slice::new_instance(%s, %s, %s)" % (
            start, stop, step
        )
