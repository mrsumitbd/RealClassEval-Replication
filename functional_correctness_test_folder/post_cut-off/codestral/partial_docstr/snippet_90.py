
import numpy as np
from PIL import Image


class LoadPilAndNumpy:
    def __init__(self, im0):
        self.paths = []
        self.im0 = []
        self.mode = 'image'
        self.bs = 0

        for i, im in enumerate(im0):
            if isinstance(im, str):
                self.paths.append(im)
                im = Image.open(im)
            else:
                self.paths.append(f'auto_{i}')
            im = self._single_check(im)
            self.im0.append(im)
        self.bs = len(self.im0)

    @staticmethod
    def _single_check(im):
        if isinstance(im, Image.Image):
            im = np.array(im)
        elif not isinstance(im, np.ndarray):
            raise TypeError("Image must be a PIL Image or a numpy array")
        if im.ndim == 2:
            im = np.expand_dims(im, axis=-1)
        if im.dtype != np.uint8:
            im = im.astype(np.uint8)
        return im

    def __len__(self):
        return self.bs

    def __next__(self):
        if not hasattr(self, '_iter'):
            self._iter = iter(zip(self.paths, self.im0, [self.mode] * self.bs))
        return next(self._iter)

    def __iter__(self):
        self._iter = iter(zip(self.paths, self.im0, [self.mode] * self.bs))
        return self
