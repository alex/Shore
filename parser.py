from collections import deque
from copy import copy


class ParseError(Exception):
    pass


class Parser(object):
    def __init__(self, tokens):
        self.tokens = deque(tokens)
        self.states = set()
    
    def parse(self):
        nodes = []
        while self.tokens:
            if self.tokens[0].name == "NEWLINE":
                self.tokens.popleft()
            else:
                nodes.append(self.statement())
        return NodeList(nodes)
    
    def first_of(self, *methods):
        for method in methods:
            try:
                return method()
            except ParseError:
                pass
        
        raise ParseError
    
    def get_token(self, name, *popped_tokens):
        tok = self.tokens.popleft()
        if tok.name != name:
            for tok in (tok,) + popped_tokens:
                self.tokens.appendleft(tok)
            raise ParseError
        return tok
        
    def statement(self):
        return self.first_of(self.simple_statement, self.compound_statement)
    
    def simple_statement(self):
        return self.first_of(self.expression, self.declaration,
            self.assignment_statement, self.flow_statement, self.import_statement)
    
    def expression(self):
        top = self.tokens.popleft()
        if top.name == "TRUE":
            return BooleanNode(True)
        elif top.name == "FALSE":
            return BooleanNode(False)
        elif top.name == "NONE":
            return NoneNode()
        elif top.name == "NAME":
            return NameNode(top.value)
        elif top.name == "NOT":
            expr = self.expression()
            return NotNode(expr)
        elif top.name == "TILDE":
            expr = self.expression()
            return NegateNode(expr)
        elif top.name == "LPAR":
            expr = self.expression()
            self.get_token("RPAR")
            return expr
        else:
            self.tokens.appendleft(top)
        
        try:
            self.first_of(self.function_call, self.literal, self.atom)
        except ParseError:
            pass
        
        # TODO: WTF happens here, all the rest of the items are of the form:
        # expression SYMBOL expression, if we call self.expression() won't we
        # recurse infinetly?
