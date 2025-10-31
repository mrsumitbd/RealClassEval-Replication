from pyparsing import Literal, one_of, Empty, printables, ParserElement, Combine, SkipTo, infix_notation, ParseFatalException, Word, nums, OpAssoc, Suppress, ParseResults, srange

class DotEmitter:

    def make_generator(self):

        def dot_gen():
            yield from printables
        return dot_gen