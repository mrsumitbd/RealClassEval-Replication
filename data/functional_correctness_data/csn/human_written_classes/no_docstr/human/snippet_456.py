import param

class WatcherSuite:

    def setup(self):

        class P(param.Parameterized):
            x0 = param.Parameter(0)

            @param.depends('x0', watch=True)
            def foo0(self):
                pass
        self.p = P()

    def time_trigger(self):
        self.p.x0 += 1