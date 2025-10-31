from pyparsing import Literal, one_of, Empty, printables, ParserElement, Combine, SkipTo, infix_notation, ParseFatalException, Word, nums, OpAssoc, Suppress, ParseResults, srange

class GroupEmitter:

    def __init__(self, exprs):
        self.exprs = ParseResults(exprs)

    def make_generator(self):

        def group_gen():

            def recurse_list(elist):
                if len(elist) == 1:
                    yield from elist[0].make_generator()()
                else:
                    for s in elist[0].make_generator()():
                        for s2 in recurse_list(elist[1:]):
                            yield (s + s2)
            if self.exprs:
                yield from recurse_list(self.exprs)
        return group_gen