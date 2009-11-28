from shore.lexer import Lexer


class PLYCompatLexer(object):
    def __init__(self, token_stream):
        self.token_stream = token_stream
    
    def token(self):
        try:
            return PLYCompatToken(self.token_stream.next())
        except StopIteration:
            return None


class PLYCompatToken(object):
    def __init__(self, token):
        self.type = token.name
        self.value = token.value
        self.lineno = None
        self.lexpos = None
    
    def __repr__(self):
        return "<Token: %r %r>" % (self.type, self.value)


class CompileError(ValueError):
    pass
