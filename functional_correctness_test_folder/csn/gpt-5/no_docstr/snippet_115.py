class Variable:

    def __init__(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not name:
            raise ValueError("name must not be empty")
        self.name = name

    def __repr__(self):
        return self.name
