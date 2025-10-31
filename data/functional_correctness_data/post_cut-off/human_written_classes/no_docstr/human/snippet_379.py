import paddle
import warnings

class UnitGaussianNormalizer:

    def __init__(self, x, eps=1e-05, reduce_dim=[0], verbose=True):
        super().__init__()
        msg = 'neuralop.utils.UnitGaussianNormalizer has been deprecated. Please use the newer neuralop.datasets.UnitGaussianNormalizer instead.'
        warnings.warn(msg, DeprecationWarning)
        n_samples, *shape = tuple(x.shape)
        self.sample_shape = shape
        self.verbose = verbose
        self.reduce_dim = reduce_dim
        self.mean = paddle.mean(x=x, axis=reduce_dim, keepdim=True).squeeze(axis=0)
        self.std = paddle.std(x=x, axis=reduce_dim, keepdim=True).squeeze(axis=0)
        self.eps = eps
        if verbose:
            print(f'UnitGaussianNormalizer init on {n_samples}, reducing over {reduce_dim}, samples of shape {shape}.')
            print(f'   Mean and std of shape {tuple(self.mean.shape)}, eps={eps}')

    def encode(self, x):
        x -= self.mean
        x /= self.std + self.eps
        return x

    def decode(self, x, sample_idx=None):
        if sample_idx is None:
            std = self.std + self.eps
            mean = self.mean
        else:
            if len(tuple(self.mean.shape)) == len(tuple(sample_idx[0].shape)):
                std = self.std[sample_idx] + self.eps
                mean = self.mean[sample_idx]
            if len(tuple(self.mean.shape)) > len(tuple(sample_idx[0].shape)):
                std = self.std[:, sample_idx] + self.eps
                mean = self.mean[:, sample_idx]
        x *= std
        x += mean
        return x

    def cuda(self):
        self.mean = self.mean.cuda(blocking=True)
        self.std = self.std.cuda(blocking=True)
        return self

    def cpu(self):
        self.mean = self.mean.cpu()
        self.std = self.std.cpu()
        return self

    def to(self, device):
        self.mean = self.mean.to(device)
        self.std = self.std.to(device)
        return self