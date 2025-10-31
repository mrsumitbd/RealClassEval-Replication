import math
from typing import Tuple, Union

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
            raise ValueError("size values must be positive integers.")
        self.auto = bool(auto)
        self.stride = int(stride)
        if self.auto and self.stride <= 0:
            raise ValueError(
                "stride must be a positive integer when auto=True.")
        # Default padding color similar to common practice (works well for uint8 images)
        self.pad_color = 114

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
        import cv2  # local import to avoid hard dependency if not used

        if not isinstance(im, np.ndarray):
            raise TypeError("Input image must be a numpy.ndarray.")
        if im.ndim not in (2, 3):
            raise ValueError(
                "Input image must have 2 or 3 dimensions (H, W[, C]).")

        # Handle grayscale by adding channel axis; remember to remove later
        squeeze_channel = False
        if im.ndim == 2:
            im = im[..., None]
            squeeze_channel = True

        ih, iw = int(im.shape[0]), int(im.shape[1])
        ch = int(im.shape[2])

        # Compute scale ratio to fit within target size
        r = min(self.h / ih, self.w / iw)
        r = max(r, 0.0)

        # Compute new unpadded size
        nh = max(int(round(ih * r)), 1)
        nw = max(int(round(iw * r)), 1)

        # Choose interpolation based on scaling direction
        interp = cv2.INTER_AREA if r < 1.0 else cv2.INTER_LINEAR
        if (ih, iw) != (nh, nw):
            im = cv2.resize(im, (nw, nh), interpolation=interp)

        # Determine final padded size
        if self.auto:
            final_h = int(math.ceil(nh / self.stride) * self.stride)
            final_w = int(math.ceil(nw / self.stride) * self.stride)
            final_h = max(final_h, self.stride)
            final_w = max(final_w, self.stride)
        else:
            final_h, final_w = self.h, self.w

        # Compute padding amounts
        dh = max(final_h - nh, 0)
        dw = max(final_w - nw, 0)

        top = dh // 2
        bottom = dh - top
        left = dw // 2
        right = dw - left

        # Determine border value based on dtype and channels
        if np.issubdtype(im.dtype, np.integer):
            pad_val = int(self.pad_color)
        else:
            pad_val = float(self.pad_color) / 255.0

        if ch == 1:
            border_value = pad_val
        else:
            border_value = (pad_val,) * ch

        im = cv2.copyMakeBorder(im, top, bottom, left, right,
                                borderType=cv2.BORDER_CONSTANT, value=border_value)

        # If needed, add extra padding to exactly match target when auto and stride rounding undershoots/overshoots
        # Ensure final shape matches requested for non-auto mode
        if not self.auto:
            # Trim any accidental overflow due to rounding
            im = im[:self.h, :self.w]

        if squeeze_channel:
            im = im[..., 0]

        return im
