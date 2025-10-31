import pyparsing as pp

class Token:

    def __init__(self, st, locn, tok_string):
        self.token_string = tok_string
        self.locn = locn
        self.source_line = pp.line(locn, st)
        self.line_no = pp.lineno(locn, st)
        self.col = pp.col(locn, st)

    def __str__(self):
        return f'{self.token_string!r} (line: {self.line_no}, col: {self.col})'