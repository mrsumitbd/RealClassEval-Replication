class Check:

    def __init__(self, args):
        self.args = args

    def __call__(self, gc, rowid, warn):
        raise NotImplementedError()