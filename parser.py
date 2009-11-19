from collections import deque


class Parser(object):
    def __init__(self, tokens):
        self.tokens = deque(tokens)
    
    @property
    def token(self):
        return self.tokens[0]
    
    def parse(self):
        nodes = []
        while self.tokens:
            if self.token.name == "newline":
                self.tokens.popleft()
            else:
                nodes.append(self.parse_statement())
        return NodeList(nodes)
    
    def parse_statement(self):
        pass
