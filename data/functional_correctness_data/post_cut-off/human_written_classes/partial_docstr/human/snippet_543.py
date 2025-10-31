import paddle

class RangeNormalizer:

    def __init__(self, x, low=0.0, high=1.0):
        super(RangeNormalizer, self).__init__()
        'Apply normaliztion to the first dimension of last axis of x\n        Input:\n            x: size(N, mesh_size, 1+d)\n        Output:\n            a: size(mesh_size)\n            b: size(mesh_size)\n        '
        x_min = (paddle.min(x=x[..., 0:1], axis=0), paddle.argmin(x=x[..., 0:1], axis=0))[0].view(-1)
        x_max = (paddle.max(x=x[..., 0:1], axis=0), paddle.argmax(x=x[..., 0:1], axis=0))[0].view(-1)
        self.a = (high - low) / (x_max - x_min)
        self.b = low - self.a * x_min

    def encode(self, x):
        """
        Input:
            x: x: size(N, mesh_size, 1+d)
        """
        d = tuple(x.shape)[-1] - 1
        x_list = paddle.split(x=x, num_or_sections=[1, d], axis=-1)
        x0_size = tuple(x_list[0].shape)
        x0 = x_list[0].reshape(x0_size[0], -1)
        x0 = self.a * x0 + self.b
        x = paddle.concat(x=[x0.reshape(x0_size), x_list[1]], axis=-1)
        return x

    def decode(self, x):
        """
        Input:
            x: size(batch*n,?) or size(T*batch*n,?)
        """
        d = tuple(x.shape)[-1] - 1
        x_list = paddle.split(x=x, num_or_sections=[1, d], axis=-1)
        x0_size = tuple(x_list[0].shape)
        x0 = x_list[0].reshape(x0_size[0], -1)
        x0 = (x0 - self.b) / self.a
        x = paddle.concat(x=[x0.reshape(x0_size), x_list[1]], axis=-1)
        return x