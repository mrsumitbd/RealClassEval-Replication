import param

class ParameterizedParamAccessSuite:

    def setup(self):

        class P1(param.Parameterized):
            x0 = param.Parameter()
        self.P1 = P1
        self.p1 = P1()

    def time_class(self):
        self.P1.param

    def time_instance(self):
        self.p1.param