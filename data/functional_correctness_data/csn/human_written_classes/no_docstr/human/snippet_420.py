class IdentityReindexer:

    def __init__(self):
        self.no_change = True

    def __call__(self, x, *args, **kwargs):
        return x