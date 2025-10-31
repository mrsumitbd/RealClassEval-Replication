class AlternativeEmitter:

    def __init__(self, exprs):
        self.exprs = exprs

    def make_generator(self):

        def alt_gen():
            for e in self.exprs:
                yield from e.make_generator()()
        return alt_gen