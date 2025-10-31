class vertex:

    def __init__(self, name, id, parents=[], children=[], meta={}):
        self.name = name
        self.id = id
        self.parents = parents
        self.children = children
        self.meta = meta

    def __str__(self):
        return self.name + '(' + str(self.id) + ').'