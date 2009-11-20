from collections import deque
from copy import copy


class Parser(object):
    def __init__(self, tokens):
        self.tokens = deque(tokens)
    
    def parse(self):
        try:
            return self.addition()
        except ParseError:
            pass
        try:
            return self.multiplication()
        except ParseError:
            pass
        
        raise ParseError()
    
    def get_token(self, name, *popped_tokens):
        tok = self.tokens.popleft()
        if tok.name != name:
            for tok in (tok,) + popped_tokens:
                self.tokens.appendleft(tok)
            raise ParseError
        return tok
    
    def addition(self):
        num = self.get_token("NUMBER")
        sym = self.get_token("PLUS", num)
        num2 = self.get_token("NUMBER", sym, num)
        return AdditionNode(num, num2)
    
    def multiplication():
        num = self.get_token("NUMBER")
        sym = self.get_token("STAR", num)
        num2 = self.get_token("NUMBER", sym, num)
        return MultiplicationNode(num, num2)

