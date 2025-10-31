import paddle

class FunActivation:

    def __init__(self, **kwrds):
        self.activation = {'Identity': paddle.nn.Identity(), 'ReLU': paddle.nn.ReLU(), 'ELU': paddle.nn.ELU(), 'Softplus': paddle.nn.Softplus(), 'Sigmoid': paddle.nn.Sigmoid(), 'Tanh': paddle.nn.Tanh(), 'SiLU': paddle.nn.Silu(), 'Swish': Swish(), 'Sinc': Sinc(), 'Tanh_Sin': Tanh_Sin()}

    def __call__(self, type=str):
        return self.activation[type]