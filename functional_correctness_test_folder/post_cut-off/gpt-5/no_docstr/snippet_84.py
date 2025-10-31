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
                "size must be an int or a tuple/list of (height, width)")
        if self.h <= 0 or self.w <= 0:
            raise ValueError("Target size must be positive integers")
        self.auto = bool(auto)
        self.stride = int(stride) if stride is not None else 32
        if self.stride <= 0:
            raise ValueError("stride must be a positive integer")

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
            raise TypeError("Input must be a numpy.ndarray")
        if im.ndim != 3:
            raise ValueError("Input image must have shape (H, W, C)")
        ih, iw, ic = im.shape
        if ic not in (1, 3, 4):
            raise ValueError("Input image must have 1, 3, or 4 channels")

        target_h, target_w = self.h, self.w
        if self.auto:
            target_h = math.ceil(target_h / self.stride) * self.stride
            target_w = math.ceil(target_w / self.stride) * self.stride

        scale = min(target_h / ih, target_w / iw)
        new_h = max(1, int(round(ih * scale)))
        new_w = max(1, int(round(iw * scale)))

        if scale != 1.0:
            interp = cv2.INTER_LINEAR if scale > 1.0 else cv2.INTER_AREA
            resized = cv2.resize(im, (new_w, new_h), interpolation=interp)
        else:
            resized = im

        pad_h = target_h - new_h
        pad_w = target_w - new_w
        if pad_h < 0 or pad_w < 0:
            # numerical safety: crop if rounding exceeded target by 1 pixel
            resized = resized[: min(new_h, target_h), : min(new_w, target_w)]
            new_h, new_w = resized.shape[:2]
            pad_h = target_h - new_h
            pad_w = target_w - new_w

        top = pad_h // 2
        bottom = pad_h - top
        left = pad_w // 2
        right = pad_w - left

        if ic == 1:
            border_val = (114,)
        elif ic == 4:
            border_val = (114, 114, 114, 0)
        else:
            border_val = (114, 114, 114)

        out = cv2.copyMakeBorder(
            resized, top, bottom, left, right, borderType=cv2.BORDER_CONSTANT, value=border_val
        )

        return out
