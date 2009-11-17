from collections import namedtuple


Symbol = namedtuple("Symbol", ["name", "value"])

class Lexer(object):
    numbers = "1234567890"
    name_start_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    name_chars = name_start_chars + numbers
    special_chars = "()[]:,+-*/|&<>=%{}~^"
    
    
    def __init__(self, text):
        self.text = text
    
    def parse(self):
        index = 0
        state = None
        current_val = []
        
        while index < len(self.text):
            ch = self.text[index]
            index += 1
            if ch == '"':
                if state == "string":
                    yield Symbol("string", "".join(current_val))
                    current_val = []
                    state = None
                    continue
                elif state == "string escaped":
                    current_val.append('"')
                    state = "string"
                    continue
                elif state is None or state == "newline":
                    state = "string"
                    continue
            elif ch in self.name_start_chars:
                if state == "string":
                    current_val.append(ch)
                    continue
                elif state == "name":
                    current_val.append(ch)
                    continue
                elif state is None or state == "newline":
                    state = "name"
                    current_val.append(ch)
                    continue
            elif ch in self.numbers:
                if state == "number":
                    current_val.append(ch)
                    continue
                elif state == "string":
                    current_val.append(ch)
                    continue
                elif state == "name":
                    current_val.append(ch)
                    continue
                elif state is None:
                    state = "number"
                    current_val.append(ch)
                    continue
            elif ch == "\n":
                if state == "name":
                    yield Symbol("name", "".join(current_val))
                    current_val = []
                elif state == "number":
                    yield Symbol("number", "".join(current_val))
                    current_val = []
                yield Symbol("newline", "\n")
                state = "newline"
                continue
            elif ch == " ":
                if state == "newline":
                    yield Symbol("whitespace", " ")
                    continue
                elif state == "name":
                    yield Symbol("name", "".join(current_val))
                    state = None
                    current_val = []
                elif state == "number":
                    yield Symbol("number", "".join(current_val))
                    state = None
                    current_val = []
            else:
                if state == "string":
                    current_val.append(ch)
                    continue
                elif state == "number":
                    yield Symbol("number", "".join(current_val))
                    state = None
                    current_val = []
                elif state == "name":
                    yield Symbol("name", "".join(current_val))
                    state = None
                    current_val = []
                yield Symbol(ch, ch)
                continue
        if state == "number":
            yield Symbol("number", "".join(current_val))
        elif state == "name":
            yield Symbol("name", "".join(current_val))
