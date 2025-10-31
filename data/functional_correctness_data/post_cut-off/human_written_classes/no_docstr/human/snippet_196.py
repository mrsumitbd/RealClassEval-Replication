import torch

class Preprocess:

    def __init__(self, size):
        self.size = size

    def __call__(self, clip):
        clip = Preprocess.resize_scale(clip, self.size[0], self.size[1], interpolation_mode='bilinear')
        return clip

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(size={self.size})'

    @staticmethod
    def resize_scale(clip, target_height, target_width, interpolation_mode):
        target_ratio = target_height / target_width
        H = clip.size(-2)
        W = clip.size(-1)
        clip_ratio = H / W
        if clip_ratio > target_ratio:
            scale_ = target_width / W
        else:
            scale_ = target_height / H
        return torch.nn.functional.interpolate(clip, scale_factor=scale_, mode=interpolation_mode, align_corners=False)