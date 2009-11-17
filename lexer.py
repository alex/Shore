from collections import namedtuple


Symbol = namedtuple("Symbol", ["name", "value"])

class Lexer(object):
    numbers = "1234567890"
    name_start_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    name_chars = name_start_chars + numbers
    special_chars = "()[]:,+-*/|&<>=%{}~^"
    
    keywords = (
        "and", "as", "break", "class", "continue", "def", "del", "elif", "else",
        "except", "finally", "for", "from", "if", "import", "in", "is", "not",
        "or", "pass", "raise", "return", "try", "while", "yield",
    )
    
    def __init__(self, text):
        self.text = text
    
    def parse(self):
        levels = [0]
        tokens = self.parse_main()
        def handle_whitespace(token):
            if len(token.value) == levels[-1]:
                return []
            elif len(token.value) > levels[-1]:
                indents = (len(token.value) - levels[-1]) / 4
                levels.append(len(token.value))
                return [Symbol("indent", "") for i in xrange(indents)]
            elif len(token.value) < levels[-1]:
                dedents = (levels[-1] - len(token.value)) / 4
                levels.append(len(token.value))
                return [Symbol("dedent", "") for i in xrange(dedents)]
        for token in tokens:
            if token.name == "newline":
                yield token
                next = tokens.next()
                if next.name == "whitespace":
                    result = handle_whitespace(next)
                    for token in result:
                        yield token
                else:
                    for i in xrange(levels[-1] / 4):
                        yield Symbol("dedent", "")
                    yield next
            else:
                yield token
                    
    
    def parse_main(self):
        index = 0
        self.state = None
        self.current_val = []
        
        while index < len(self.text):
            ch = self.text[index]
            index += 1
            
            if self.state is not None:
                result = getattr(self, self.state)(ch)
            else:
                result = self.generic(ch)
            
            if result is not None:
                if not isinstance(result, list):
                    result = [result]
                for result in result:
                    if result is not None:
                        yield result

        if self.state == "number":
            yield Symbol("number", "".join(self.current_val))
        elif self.state == "name":
            yield Symbol("name", "".join(self.current_val))
    
    def emit_name(self):
        name = "".join(self.current_val)
        self.current_val = []
        if name in self.keywords:
            return Symbol(name, name)
        return Symbol("name", name)
    
    def string(self, ch):
        if ch == '"':
            sym = Symbol("string", "".join(self.current_val))
            self.current_val = []
            self.state = None
            return sym
        elif ch == "\\":
            self.state = "string_escaped"
        else:
            self.current_val.append(ch)
    
    def string_escaped(self, ch):
        self.current_val.append(ch)
        self.state = "string"
    
    def name(self, ch):
        if ch in self.name_chars:
            self.current_val.append(ch)
        else:
            sym = self.emit_name()
            self.state = None
            return [sym, self.generic(ch)]
    
    def number(self, ch):
        if ch in self.numbers:
            self.current_val.append(ch)
        else:
            sym = Symbol("number", "".join(self.current_val))
            self.current_val = []
            self.state = None
            return [sym, self.generic(ch)]
    
    def newline(self, ch):
        if ch == " ":
            self.current_val.append(" ")
        else:
            if self.current_val:
                sym = Symbol("whitespace", "".join(self.current_val))
                self.state = None
                self.current_val = []
                return [sym, self.generic(ch)]
            return self.generic(ch)
    
    def generic(self, ch):
        if ch == '"':
            self.state = "string"
        elif ch in self.name_start_chars:
            self.state = "name"
            self.current_val.append(ch)
        elif ch in self.numbers:
            self.state = "number"
            self.current_val.append(ch)
        elif ch == " ":
            return
        elif ch == "\n":
            self.state = "newline"
            return Symbol("newline", "\n")
        else:
            return Symbol(ch, ch)
