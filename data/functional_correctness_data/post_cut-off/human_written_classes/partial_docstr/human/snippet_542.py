import paddle

class GaussianNormalizer:

    def __init__(self, x, eps=1e-08):
        super(GaussianNormalizer, self).__init__
        'Apply normaliztion to the first dimension of last axis of x\n        Input:\n            x: size(N, mesh_size, 1+d)\n        Output:\n            mean: size()\n            std: size()\n        '
        self.mean = paddle.mean(x=x[..., 0])
        self.std = paddle.std(x=x[..., 0])
        self.eps = eps

    def encode(self, x):
        """
        Input:
            x: x: size(N, mesh_size, 1+d)
        """
        d = tuple(x.shape)[-1] - 1
        x_list = paddle.split(x=x, num_or_sections=[1, d], axis=-1)
        x = paddle.concat(x=[(x_list[0] - self.mean) / (self.std + self.eps), x_list[1]], axis=-1)
        return x

    def decode(self, x):
        """
        Input:
            x: size(batch*n,?) or size(T*batch*n,?)
        """
        d = tuple(x.shape)[-1] - 1
        x_list = paddle.split(x=x, num_or_sections=[1, d], axis=-1)
        x = paddle.concat(x=[x_list[0] * (self.std + self.eps) + self.mean, x_list[1]], axis=-1)
        return x