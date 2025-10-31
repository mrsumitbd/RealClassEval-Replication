
import numpy as np
import torch


class ToTensor:
    def __init__(self, half=False):
        self.half = half

    def __call__(self, im):
        # Convert BGR to RGB
        im = im[:, :, ::-1]
        # Normalize to [0, 1]
        im = im / 255.0
        # Convert to tensor
        im = torch.from_numpy(im).permute(2, 0, 1)
        # Convert to half precision if required
        if self.half:
            im = im.half()
        return im
