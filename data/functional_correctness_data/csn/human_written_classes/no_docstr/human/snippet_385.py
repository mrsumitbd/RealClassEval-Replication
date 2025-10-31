class Calc:

    def __init__(self, **kwargs):
        self.assignments = kwargs.pop('assignments')
        self.expression = kwargs.pop('expression')

    @property
    def value(self):
        for a in self.assignments:
            namespace[a.variable] = a.expression.value
        return self.expression.value