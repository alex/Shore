from collections import deque
from copy import copy


class Parser(object):
    def __init__(self, tokens):
        self.tokens = deque(tokens)
        self.states = set()
    
    def parse(self):
        self.states.add((self.main_parse, self.tokens))
        # While there's more than one next state, or if there's a single state
        # that state has tokens
        while len(self.states) > 1 and not iter(self.states).next()[1]:
            next_state, tokens = self.states.pop()
            next_state(tokens)
        state = self.states.pop()
        return state
    
    def main_parse(self, tokens):
        nodes = []
        while tokens:
            if tokens[0].name == "newline":
                tokens.popleft()
            else:
                nodes.append(self.parse_statement(copy(tokens)))
        return NodeList(nodes)
    
    def parse_statement(self, tokens):
        self.states.add((self.simple_statement, copy(tokens)))
        self.states.add((self.compound_statement, copy(tokens))
    
    def simple_statement(self, tokens):
        self.states.add((self.expression, copy(tokens)))
        self.states.add((self.decleration, copy(tokens))
        self.states.add((self.assignment_statement, copy(tokens))
        self.states.add((self.flow_statement, copy(tokens))
        self.states.add((self.import_statement, copy(tokens))
