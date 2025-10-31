
import numpy as np
from PIL import Image


class CenterCrop:
    def __init__(self, size=640):
        if isinstance(size, int):
            self.h = size
            self.w = size
        elif isinstance(size, tuple) and len(size) == 2:
            self.h, self.w = size
        else:
            raise ValueError(
                "Size must be an integer or a tuple of two integers.")

    def __call__(self, im):
        if isinstance(im, np.ndarray):
            h, w, c = im.shape
        elif isinstance(im, Image.Image):
            w, h = im.size
            c = len(im.getbands())
        else:
            raise ValueError(
                "Input image must be a numpy array or a PIL Image object.")

        ratio = min(self.h / h, self.w / w)
        new_h, new_w = int(h * ratio), int(w * ratio)
        top = (h - new_h) // 2
        left = (w - new_w) // 2

        if isinstance(im, np.ndarray):
            cropped_im = im[top:top+new_h, left:left+new_w, :]
            resized_im = np.array(Image.fromarray(
                cropped_im).resize((self.w, self.h), Image.BILINEAR))
        elif isinstance(im, Image.Image):
            cropped_im = im.crop((left, top, left+new_w, top+new_h))
            resized_im = np.array(cropped_im.resize(
                (self.w, self.h), Image.BILINEAR))

        return resized_im
