class Exprs:
    """A parsed list of exprs"""

    def __init__(self, string):
        self.ast = _parse(string)
        self.as_string = None
        if len(self.ast) == 1 and isinstance(self.ast[0], str):
            self.as_string = self.ast[0]

    @staticmethod
    def _expand(ast, flag_defs):
        """Expand ast for the given flag_defs.

        Returns a (possibly empty) list of strings

        """
        expanded = []
        for child in ast:
            if isinstance(child, str):
                expanded.append(child)
                continue
            negated, flag, exprs = child
            if (flag in flag_defs) == negated:
                continue
            expanded += Exprs._expand(exprs, flag_defs)
        return expanded

    @staticmethod
    def _flags_to_flag_defs(flags):
        """Convert a flags dictionary to the set of flags that are defined"""
        ret = []
        for k, v in flags.items():
            if v is True:
                ret.append(k)
            elif v not in [False, None]:
                ret.append(k + '_' + v)
        return set(ret)

    def expand(self, flags):
        """Expand the parsed string in the presence of the given flags"""
        if self.as_string is not None:
            return self.as_string
        flag_defs = Exprs._flags_to_flag_defs(flags)
        return ' '.join(Exprs._expand(self.ast, flag_defs))