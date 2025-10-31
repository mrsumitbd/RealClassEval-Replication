class Register:
    """Abstraction for a register in the VM.

    Members:
    node          -- the AST node this corresponds to
    temporary     -- True if this isn't an input or output
    immediate     -- not a register, but an immediate value
    n             -- the physical register number.
                     None if no number assigned yet.
    """

    def __init__(self, astnode, temporary=False):
        self.node = astnode
        self.temporary = temporary
        self.immediate = False
        self.n = None

    def __str__(self):
        if self.temporary:
            name = 'Temporary'
        else:
            name = 'Register'
        return '%s(%s, %s, %s)' % (name, self.node.astType, self.node.astKind, self.n)

    def __repr__(self):
        return self.__str__()