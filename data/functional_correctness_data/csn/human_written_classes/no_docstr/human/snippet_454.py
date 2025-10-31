import param

class ParameterizedParamContainsSuite:

    def setup(self):

        class P1(param.Parameterized):
            x0 = param.Parameter()
            x1 = param.Parameter()
            x2 = param.Parameter()
            x3 = param.Parameter()
            x4 = param.Parameter()
            x5 = param.Parameter()
        self.P1 = P1
        self.p1 = P1()

    def time_class(self):
        'x5' in self.P1.param

    def time_instance(self):
        'x5' in self.p1.param