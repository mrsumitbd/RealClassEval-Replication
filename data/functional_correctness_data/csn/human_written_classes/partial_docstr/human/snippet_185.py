class RawNode:
    """
    Used to pass raw integers to interpreter.
    For instance, for selecting what function to use in func1.
    Purposely don't inherit from ExpressionNode, since we don't wan't
    this to be used for anything but being walked.
    """
    astType = 'raw'
    astKind = 'none'

    def __init__(self, value):
        self.value = value
        self.children = ()

    def __str__(self):
        return 'RawNode(%s)' % (self.value,)
    __repr__ = __str__