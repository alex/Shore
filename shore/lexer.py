from collections import namedtuple


class Symbol(namedtuple("Symbol", ["name", "value", "lineno"])):
    def __eq__(self, other):
        return self[:-1] == other


def token_processor(func):
    def parser(inner_func):
        def inner(self):
            tokens = inner_func(self)
            return func(tokens)
        return inner
    return parser

@token_processor
def track_indents(tokens):
    levels = [0]
    def handle_whitespace(token):
        if len(token.value) == levels[-1]:
            return []
        elif len(token.value) > levels[-1]:
            indents = (len(token.value) - levels[-1]) / 4
            levels.append(len(token.value))
            return [Symbol("INDENT", "", token.lineno) for i in xrange(indents)]
        elif len(token.value) < levels[-1]:
            dedents = (levels[-1] - len(token.value)) / 4
            levels.append(len(token.value))
            return [Symbol("DEDENT", "", token.lineno) for i in xrange(dedents)]
    for token in tokens:
        if token.name == "NEWLINE":
            yield token
            next = tokens.next()
            if next.name == "WHITESPACE":
                result = handle_whitespace(next)
                for token in result:
                    yield token
            else:
                for i in xrange(levels[-1] / 4):
                    yield Symbol("DEDENT", "", token.lineno)
                levels.append(0)
                yield next
        else:
            yield token
    yield Symbol("NEWLINE", "\n", token.lineno)
    for i in xrange(levels[-1] / 4):
        yield Symbol("DEDENT", "", token.lineno)


@token_processor
def combine_is_not(tokens):
    for token in tokens:
        if token.name == "IS":
            next = tokens.next()
            if next.name == "NOT":
                yield Symbol("ISNOT", "is not", token.lineno)
            else:
                yield token
                yield next
        else:
            yield token

class Lexer(object):
    numbers = "1234567890"
    name_start_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    name_chars = name_start_chars + numbers
    
    keywords = frozenset([
        "and", "break", "class", "continue", "def", "elif", "else",
        "except", "finally", "for", "from", "if", "import", "in", "is", "not",
        "or", "pass", "raise", "return", "try", "while", "yield", "True",
        "False", "None", "isnot", # "as", "with",
    ])
    
    symbols = {
        "@": "DECORATOR",
        "+": "PLUS",
        "-": "MINUS",
        "*": "STAR",
        "/": "SLASH",
        "(": "LPAR",
        ")": "RPAR",
        "[": "LSQB",
        "]": "RSQB",
        ":": "COLON",
        ",": "COMMA",
        "|": "VBAR",
        "&": "AMPER",
        "<": "LESS",
        ">": "GREATER",
        "=": "EQUAL",
        ".": "DOT",
        "%": "PERCENT",
        "{": "LBRACE",
        "}": "RBRACE",
        "~": "TILDE",
        "^": "CIRCUMFLEX",
        "@": "AT",
        "**": "STARSTAR",
        "!=": "NE",
        "==": "EQEQ",
        "<=": "LE",
        ">=": "GE",
    }
    
    # These are the start characters for various 2 char symbols, such as STAR STAR.
    long_symbols = frozenset("*!=<>")
    
    tokens = list(set(["NUMBER", "NAME", "INDENT", "DEDENT", "STRING", "NEWLINE"]) |
        set(symbols.values()) | set(map(lambda s: s.upper(), keywords)))
    
    def __init__(self, text):
        self.text = text        
    
    @combine_is_not
    @track_indents
    def tokenize(self):
        index = 0
        self.state = None
        self.current_val = []
        self.lineno = 1
        
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
            yield Symbol("NUMBER", "".join(self.current_val), self.lineno)
        elif self.state == "name":
            yield self.emit_name()
        elif self.state == "long_symbol":
            ch = self.current_val.pop()
            yield Symbol(self.symbols[ch].upper(), ch, self.lineno)
            
    def emit_name(self):
        name = "".join(self.current_val)
        self.current_val = []
        if name in self.keywords:
            return Symbol(name.upper(), name, self.lineno)
        return Symbol("NAME", name, self.lineno)
    
    def string(self, ch):
        if ch == '"':
            sym = Symbol("STRING", "".join(self.current_val), self.lineno)
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
            sym = Symbol("NUMBER", "".join(self.current_val), self.lineno)
            self.current_val = []
            self.state = None
            return [sym, self.generic(ch)]
    
    def newline(self, ch):
        if ch == " ":
            self.current_val.append(" ")
        else:
            if self.current_val:
                sym = Symbol("WHITESPACE", "".join(self.current_val), self.lineno)
                self.state = None
                self.current_val = []
                return [sym, self.generic(ch)]
            return self.generic(ch)
    
    def long_symbol(self, ch):
        old_ch = self.current_val.pop()
        val = old_ch + ch
        if val in self.symbols:
            sym = Symbol(self.symbols[val].upper(), val, self.lineno)
            self.state = None
            return sym
        self.state = None
        return [Symbol(self.symbols[old_ch].upper(), old_ch, self.lineno), self.generic(ch)]
    
    def comment(self, ch):
        if ch != "\n":
            return
        self.state = None
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
            self.lineno += 1
            return Symbol("NEWLINE", "\n", self.lineno)
        elif ch == "#":
            self.state = "comment"
            return
        else:
            if ch in self.long_symbols:
                self.state = "long_symbol"
                self.current_val.append(ch)
                return
            if ch in self.symbols:
                return Symbol(self.symbols[ch].upper(), ch, self.lineno)
            raise ValueError("%s couldn't be parsed" % ch)
