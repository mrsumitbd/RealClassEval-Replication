class CallableString:

    def __init__(self, s):
        self.s = s

    def __call__(self, *args, **kwargs):
        return self.s