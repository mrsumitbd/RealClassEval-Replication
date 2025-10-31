class SemanticGroup:

    def __init__(self, contents):
        self.contents = contents
        while self.contents[-1].__class__ == self.__class__:
            self.contents = self.contents[:-1] + self.contents[-1].contents

    def __str__(self):
        return '{}({})'.format(self.label, ' '.join([isinstance(c, str) and c or str(c) for c in self.contents]))