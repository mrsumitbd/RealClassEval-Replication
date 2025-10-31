import paddle

class UnitGaussianNormalizer:

    def __init__(self, x, eps=1e-08):
        super(UnitGaussianNormalizer, self).__init__()
        'Apply normaliztion to the first dimension of last axis of x\n        Input:\n            x: size(N, mesh_size, 1+d)\n        Output:\n            mean: size(mesh_szie, 1)\n            std: size(mesh_size, 1)\n        '
        self.mean = paddle.mean(x=x[..., 0:1], axis=0)
        self.std = paddle.std(x=x[..., 0:1], axis=0)
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

    def decode(self, x, sample_idx=None):
        """ """
        if sample_idx is not None:
            if len(tuple(self.mean.shape)) == len(tuple(sample_idx[0].shape)):
                std = self.std[sample_idx]
                mean = self.mean[sample_idx]
            if len(tuple(self.mean.shape)) > len(tuple(sample_idx[0].shape)):
                std = self.std[:, sample_idx]
                mean = self.mean[:, sample_idx]
        else:
            std = self.std
            mean = self.mean
        d = tuple(x.shape)[-1] - 1
        x_list = paddle.split(x=x, num_or_sections=[1, d], axis=-1)
        x = paddle.concat(x=[x_list[0] * (std + self.eps) + mean, x_list[1]], axis=-1)
        return x