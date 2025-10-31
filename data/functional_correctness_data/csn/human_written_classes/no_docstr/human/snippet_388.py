class RRELExpression:

    def __init__(self, seq, flags):
        self.seq = seq
        self.flags = flags
        self.importURI = 'm' in flags
        self.use_proxy = 'p' in flags

        def prepare_tree(node):
            if isinstance(node, RRELNavigation):
                node.rrel_expression = self
            if isinstance(node, RRELBase):
                for c in node.__dict__.values():
                    if isinstance(c, list):
                        for e in c:
                            prepare_tree(e)
                    else:
                        prepare_tree(c)
        prepare_tree(self.seq)

    def __repr__(self):
        if self.importURI:
            return '+' + self.flags + ':' + str(self.seq)
        else:
            return str(self.seq)