class Arguments:
    """Represents arguments of a function."""

    def __init__(self, args):
        """Argument container class.

        Args:
            args(list(ast.args): The arguments in a function AST node.
        """
        self.args = args.args
        self.varargs = args.vararg
        self.kwarg = args.kwarg
        self.kwonlyargs = args.kwonlyargs
        self.defaults = args.defaults
        self.kw_defaults = args.kw_defaults
        self.arguments = list()
        if self.args:
            self.arguments.extend([x.arg for x in self.args])
        if self.varargs:
            self.arguments.extend(self.varargs.arg)
        if self.kwarg:
            self.arguments.extend(self.kwarg.arg)
        if self.kwonlyargs:
            self.arguments.extend([x.arg for x in self.kwonlyargs])

    def __getitem__(self, key):
        return self.arguments.__getitem__(key)

    def __len__(self):
        return self.args.__len__()