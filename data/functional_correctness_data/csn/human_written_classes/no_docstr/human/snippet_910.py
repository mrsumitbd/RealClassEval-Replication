class placeholder:

    def __init__(self, val):
        if val not in ['input', 'msfile', 'output']:
            raise ValueError('Only accepts input, output or msfile for placeholder argument')
        self.__val = val

    def __call__(self):
        return self.__val

    def __get__(self):
        return self.__val

    def __repr__(self):
        return 'Placeholder(type {})'.format(self.__val)