
import numpy as np
import cv2


class ClassifyLetterBox:
    def __init__(self, size=(640, 640), auto=False, stride=32):
        if isinstance(size, int):
            self.h = size
            self.w = size
        else:
            self.h, self.w = size
        self.auto = auto
        self.stride = stride

    def __call__(self, im):
        if self.auto:
            self.h = self.h // self.stride * self.stride
            self.w = self.w // self.stride * self.stride

        shape = im.shape[:2]
        r = min(self.h / shape[0], self.w / shape[1])
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = self.w - new_unpad[0], self.h - new_unpad[1]

        dw /= 2
        dh /= 2

        if shape[::-1] != new_unpad:
            im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        im = cv2.copyMakeBorder(
            im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))

        return im
