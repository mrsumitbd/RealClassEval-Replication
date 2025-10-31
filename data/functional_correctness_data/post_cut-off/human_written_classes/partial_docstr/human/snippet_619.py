import random
import numpy as np
import torch

class ApplyDeeperForensicsDistortion:
    """Wrapper for applying DeeperForensics distortions."""

    def __init__(self, distortion_type, level_min=0, level_max=3):
        self.distortion_type = distortion_type
        self.level_min = level_min
        self.level_max = level_max

    def __call__(self, img, level=None):
        if level is None:
            self.level = random.randint(self.level_min, self.level_max)
        else:
            self.level = level
        if self.level > 0:
            self.distortion_param = get_distortion_parameter(self.distortion_type, self.level)
            self.distortion_func = get_distortion_function(self.distortion_type)
        else:
            self.distortion_func = None
            self.distortion_param = None
        if not self.distortion_func:
            return img
        if isinstance(img, torch.Tensor):
            img = rgb_to_bgr(img)
            img = img.permute(1, 2, 0).cpu().numpy()
            img = (img * 255).astype(np.uint8)
        img = self.distortion_func(img, self.distortion_param)
        if isinstance(img, np.ndarray):
            img = torch.from_numpy(img.astype(np.float32) / 255.0)
            img = img.permute(2, 0, 1)
            img = bgr_to_rgb(img)
        return img