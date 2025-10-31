import math
from typing import Tuple, Union

import numpy as np

try:
    import cv2
except Exception:
    cv2 = None


class ClassifyLetterBox:
    '''
    A class for resizing and padding images for classification tasks.
    This class is designed to be part of a transformation pipeline, e.g., T.Compose([LetterBox(size), ToTensor()]).
    It resizes and pads images to a specified size while maintaining the original aspect ratio.
    Attributes:
        h (int): Target height of the image.
        w (int): Target width of the image.
        auto (bool): If True, automatically calculates the short side using stride.
        stride (int): The stride value, used when 'auto' is True.
    Methods:
        __call__: Applies the letterbox transformation to an input image.
    Examples:
        >>> transform = ClassifyLetterBox(size=(640, 640), auto=False, stride=32)
        >>> img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        >>> result = transform(img)
        >>> print(result.shape)
        (640, 640, 3)
    '''

    def __init__(self, size: Union[int, Tuple[int, int]] = (640, 640), auto: bool = False, stride: int = 32):
        '''
        Initializes the ClassifyLetterBox object for image preprocessing.
        This class is designed to be part of a transformation pipeline for image classification tasks. It resizes and
        pads images to a specified size while maintaining the original aspect ratio.
        Args:
            size (int | Tuple[int, int]): Target size for the letterboxed image. If an int, a square image of
                (size, size) is created. If a tuple, it should be (height, width).
            auto (bool): If True, automatically calculates the short side based on stride. Default is False.
            stride (int): The stride value, used when 'auto' is True. Default is 32.
        Attributes:
            h (int): Target height of the letterboxed image.
            w (int): Target width of the letterboxed image.
            auto (bool): Flag indicating whether to automatically calculate short side.
            stride (int): Stride value for automatic short side calculation.
        Examples:
            >>> transform = ClassifyLetterBox(size=224)
            >>> img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            >>> result = transform(img)
            >>> print(result.shape)
            (224, 224, 3)
        '''
        if isinstance(size, int):
            h, w = size, size
        elif isinstance(size, (tuple, list)) and len(size) == 2:
            h, w = int(size[0]), int(size[1])
        else:
            raise ValueError(
                "size must be an int or a tuple of two ints (h, w)")

        if h <= 0 or w <= 0:
            raise ValueError(
                "Target size dimensions must be positive integers")

        if not isinstance(auto, bool):
            raise TypeError("auto must be a boolean")

        if not isinstance(stride, int) or stride <= 0:
            raise ValueError("stride must be a positive integer")

        self.h = h
        self.w = w
        self.auto = auto
        self.stride = stride

    def __call__(self, im: np.ndarray) -> np.ndarray:
        '''
        Resizes and pads an image using the letterbox method.
        This method resizes the input image to fit within the specified dimensions while maintaining its aspect ratio,
        then pads the resized image to match the target size.
        Args:
            im (numpy.ndarray): Input image as a numpy array with shape (H, W, C).
        Returns:
            (numpy.ndarray): Resized and padded image as a numpy array with shape (hs, ws, 3), where hs and ws are
                the target height and width respectively.
        Examples:
            >>> letterbox = ClassifyLetterBox(size=(640, 640))
            >>> image = np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)
            >>> resized_image = letterbox(image)
            >>> print(resized_image.shape)
            (640, 640, 3)
        '''
        if not isinstance(im, np.ndarray):
            raise TypeError("Input image must be a numpy.ndarray")
        if im.ndim != 3 or im.shape[2] not in (1, 3, 4):
            raise ValueError(
                "Input image must have shape (H, W, C) with C in {1, 3, 4}")

        ih, iw = int(im.shape[0]), int(im.shape[1])
        if ih == 0 or iw == 0:
            raise ValueError("Input image has invalid dimensions")

        # Compute scale to fit within target while keeping aspect ratio
        r = min(self.h / ih, self.w / iw)
        new_h = max(1, int(round(ih * r)))
        new_w = max(1, int(round(iw * r)))

        # Resize
        if cv2 is not None:
            if r > 1.0:
                interp = cv2.INTER_LINEAR
            else:
                interp = cv2.INTER_AREA
            resized = cv2.resize(im, (new_w, new_h), interpolation=interp)
        else:
            # Fallback to PIL if cv2 is unavailable
            from PIL import Image
            pil_im = Image.fromarray(im)
            resample = Image.BILINEAR if r > 1.0 else Image.BOX
            resized = np.array(pil_im.resize(
                (new_w, new_h), resample=resample))

        # Optionally adjust final canvas to be aligned to stride
        if self.auto and self.stride > 1:
            hs = new_h + ((self.h - new_h) % self.stride)
            ws = new_w + ((self.w - new_w) % self.stride)
        else:
            hs, ws = self.h, self.w

        pad_h = max(0, hs - new_h)
        pad_w = max(0, ws - new_w)

        top = pad_h // 2
        bottom = pad_h - top
        left = pad_w // 2
        right = pad_w - left

        # Ensure dtype and channels
        if resized.dtype != np.uint8:
            resized = resized.astype(np.uint8)

        # Pad
        if cv2 is not None:
            color = (114, 114, 114)
            padded = cv2.copyMakeBorder(
                resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)
        else:
            if resized.ndim == 2:
                pad_width = ((top, bottom), (left, right))
                padded = np.pad(resized, pad_width,
                                mode="constant", constant_values=114)
            else:
                c = resized.shape[2]
                pad_width = ((top, bottom), (left, right), (0, 0))
                padded = np.pad(resized, pad_width, mode="constant",
                                constant_values=((114, 114), (114, 114), (0, 0)))
                if c in (3, 4):
                    for ch in range(c):
                        if ch < 3:
                            padded[..., ch] = np.pad(
                                resized[..., ch], ((top, bottom), (left, right)), mode="constant", constant_values=114
                            )
                        else:
                            padded[..., ch] = np.pad(
                                resized[..., ch], ((top, bottom), (left, right)), mode="constant", constant_values=0
                            )

        return padded[:hs, :ws, ...] if padded.ndim == 3 else padded[:hs, :ws]
