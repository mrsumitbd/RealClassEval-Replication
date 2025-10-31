from PyDC.PyDC.utils import LOG_FORMATTER, LOG_LEVEL_DICT, codepoints2string, get_word, iter_steps, pformat_codepoints, string2codepoint

class CodeLine:

    def __init__(self, line_pointer, line_no, code):
        assert isinstance(line_no, int), f"Line number not integer, it's: {repr(line_no)}"
        self.line_pointer = line_pointer
        self.line_no = line_no
        self.code = code

    def get_ascii_codeline(self):
        return f'{self.line_no:d} {self.code}'

    def get_as_codepoints(self):
        return tuple(string2codepoint(self.get_ascii_codeline()))

    def __repr__(self):
        return f'<CodeLine pointer: {repr(self.line_pointer)} line no: {repr(self.line_no)} code: {repr(self.code)}>'