from shore.lexer import Lexer


class PLYCompatLexer(object):
    def __init__(self, text):
        self.text = text
        self.token_stream = Lexer(text).parse()
    
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
