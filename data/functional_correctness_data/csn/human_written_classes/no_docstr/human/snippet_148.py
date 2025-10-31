class OptionalEmitter:

    def __init__(self, expr):
        self.expr = expr

    def make_generator(self):

        def optional_gen():
            yield ''
            yield from self.expr.make_generator()()
        return optional_gen