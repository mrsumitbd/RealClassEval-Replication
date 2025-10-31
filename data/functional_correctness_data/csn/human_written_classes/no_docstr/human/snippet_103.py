import dynet as dy

class DynetLinear:

    def __init__(self, dim_in, dim_out, dyParameterCollection):
        assert isinstance(dyParameterCollection, dy.ParameterCollection)
        self.dim_in = dim_in
        self.dim_out = dim_out
        self.pW = dyParameterCollection.add_parameters((dim_out, dim_in))
        self.pb = dyParameterCollection.add_parameters(dim_out)

    def __call__(self, x):
        assert isinstance(x, dy.Expression)
        self.W = dy.parameter(self.pW)
        self.b = dy.parameter(self.pb)
        self.x = x
        return self.W * self.x + self.b