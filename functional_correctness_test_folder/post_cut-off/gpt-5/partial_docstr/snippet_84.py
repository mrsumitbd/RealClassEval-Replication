import math
from typing import Tuple, Union

import cv2
import numpy as np


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
            self.h, self.w = size, size
        elif isinstance(size, (tuple, list)) and len(size) == 2:
            self.h, self.w = int(size[0]), int(size[1])
        else:
            raise ValueError(
                "size must be an int or a tuple/list of (height, width).")
        if self.h <= 0 or self.w <= 0:
            raise ValueError("size dimensions must be positive.")
        self.auto = bool(auto)
        self.stride = int(stride) if stride is not None else 32
        if self.stride <= 0:
            raise ValueError("stride must be a positive integer.")

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
            raise TypeError("Input must be a numpy ndarray.")
        if im.ndim == 2:
            im = im[..., None]
        if im.ndim != 3:
            raise ValueError("Input image must have shape (H, W, C).")
        ih, iw, c = im.shape
        if c not in (1, 3, 4):
            raise ValueError("Input image must have 1, 3, or 4 channels.")

        # Determine scale
        if self.auto:
            target_long = max(self.h, self.w)
            r = target_long / max(ih, iw)
        else:
            r = min(self.h / ih, self.w / iw)

        newh = max(1, int(round(ih * r)))
        neww = max(1, int(round(iw * r)))

        # Choose interpolation
        if r > 1.0:
            interp = cv2.INTER_LINEAR
        else:
            interp = cv2.INTER_AREA

        resized = cv2.resize(im, (neww, newh), interpolation=interp)

        if self.auto:
            final_h = int(math.ceil(newh / self.stride) * self.stride)
            final_w = int(math.ceil(neww / self.stride) * self.stride)
        else:
            final_h, final_w = self.h, self.w

        pad_h = max(0, final_h - newh)
        pad_w = max(0, final_w - neww)

        top = pad_h // 2
        bottom = pad_h - top
        left = pad_w // 2
        right = pad_w - left

        if np.issubdtype(resized.dtype, np.integer):
            fill_val = 114
        else:
            fill_val = 114.0 / 255.0

        if c == 1:
            border_value = fill_val
        else:
            if c == 4:
                border_value = (fill_val, fill_val, fill_val, 0 if np.issubdtype(
                    resized.dtype, np.integer) else 0.0)
            else:
                border_value = (fill_val, fill_val, fill_val)

        padded = cv2.copyMakeBorder(
            resized, top, bottom, left, right, borderType=cv2.BORDER_CONSTANT, value=border_value
        )

        return padded[:final_h, :final_w, :]
