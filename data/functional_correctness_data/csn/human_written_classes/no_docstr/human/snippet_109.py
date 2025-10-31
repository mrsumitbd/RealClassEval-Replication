class Parent:

    def __init__(self, type, indent, line_indent=None):
        self.type = type
        self.indent = indent
        self.line_indent = line_indent
        self.explicit_key = False
        self.implicit_block_seq = False

    def __repr__(self):
        return f'{labels[self.type]}:{self.indent}'