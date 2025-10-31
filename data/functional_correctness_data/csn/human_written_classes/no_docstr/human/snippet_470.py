class _picklable_f:

    def __init__(self, fun):
        self.fun = fun

    def __call__(self, **kwargs):
        pf = SMC(**kwargs)
        pf.run()
        return self.fun(pf)