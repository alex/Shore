class Context(object):
    def __init__(self):
        self.dicts = []
    
    def push(self):
        self.dicts.append({})
    
    def pop(self):
        self.dicts.pop()
    
    def __setitem__(self, name, item):
        self.dicts[-1][name] = item
    
    def __getitem__(self, name):
        for dict_ in reversed(self.dicts):
            if name in dict_:
                return dict_[name]
        raise KeyError
    
    def __contains__(self, name):
        try:
            self[name]
            return True
        except KeyError:
            return False
