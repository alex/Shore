import itertools

from shore import ast
from shore.utils import CompileError


class Module(object):
    def __init__(self, name):
        self.name = name
        self.variables = {}
        self.functions = {}
        self.classes = {}
        self.templates = {}

    def add_builtins(self, classes, functions):
        for name, class_ in classes.iteritems():
            self.classes[name] = class_
        for name, function in functions.iteritems():
            self.functions[name] = function
    
    def check_name(self, name):
        if name in (set(self.variables) | set(self.functions) | set(self.classes)):
            raise CompileError("%s already defined in %s, fail." % (name, self.name))
    
    def add_variables(self, node):
        self.check_name(node.name)
        self.variables[node.name] = node
    
    def add_function(self, node):
        self.check_name(node.name)
        if node.templates:
            self.templates[node.name] = node
        else:
            self.functions[node.name] = node
    
    def add_class(self, node):
        self.check_name(node.name)
        if node.templates:
            self.templates[node.name] = node
        else:
            self.classes[node.name] = node
    
    def from_ast(self, nodelist):
        for node in nodelist.nodes:
            if isinstance(node, ast.DeclarationNode):
                self.add_variables(node)
            elif isinstance(node, ast.FunctionNode):
                self.add_function(node)
            elif isinstance(node, ast.ClassNode):
                self.add_class(node)
            else:
                raise CompileError("You have stuff in the global scope that "
                    "isn't a declaraion of some sort")
        
        for obj in itertools.chain(self.functions.itervalues(), self.classes.itervalues()):
            obj.bind_to_module(self)
        
        for obj in itertools.chain(self.functions.itervalues(), self.classes.itervalues()):
            obj.verify()
    
    def generate_code(self):
        code = [
            '#include "builtins.h"',
            '#include "frame.h"',
            '#include "object.h"',
            '#include "state.h"',
        ]
        
        code.append("std::vector<shore::Frame*> shore::State::frames;")
        code.append("shore::GCSet shore::GC::allocated_objects;")
        for class_ in self.classes.values():
            code.extend(class_.generate_code())
        
        for function in self.functions.values():
            code.extend(function.get_frame_class())
        for function in self.functions.values():
            code.extend(function.generate_code())
        
        return "\n".join(code)
