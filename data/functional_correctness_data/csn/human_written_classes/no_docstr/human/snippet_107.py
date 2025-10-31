import yaml

class Comment:

    def __init__(self, line_no, column_no, buffer, pointer, token_before=None, token_after=None, comment_before=None):
        self.line_no = line_no
        self.column_no = column_no
        self.buffer = buffer
        self.pointer = pointer
        self.token_before = token_before
        self.token_after = token_after
        self.comment_before = comment_before

    def __str__(self):
        end = self.buffer.find('\n', self.pointer)
        if end == -1:
            end = self.buffer.find('\x00', self.pointer)
        if end != -1:
            return self.buffer[self.pointer:end]
        return self.buffer[self.pointer:]

    def __eq__(self, other):
        return isinstance(other, Comment) and self.line_no == other.line_no and (self.column_no == other.column_no) and (str(self) == str(other))

    def is_inline(self):
        return not isinstance(self.token_before, yaml.StreamStartToken) and self.line_no == self.token_before.end_mark.line + 1 and (self.buffer[self.token_before.end_mark.pointer - 1] != '\n')