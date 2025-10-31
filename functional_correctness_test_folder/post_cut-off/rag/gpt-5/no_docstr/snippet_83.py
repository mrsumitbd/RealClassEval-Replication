import math
from typing import Tuple, Union

import numpy as np
import cv2
from PIL import Image


class CenterCrop:
    '''
    Applies center cropping to images for classification tasks.
    This class performs center cropping on input images, resizing them to a specified size while maintaining the aspect
    ratio. It is designed to be part of a transformation pipeline, e.g., T.Compose([CenterCrop(size), ToTensor()]).
    Attributes:
        h (int): Target height of the cropped image.
        w (int): Target width of the cropped image.
    Methods:
        __call__: Applies the center crop transformation to an input image.
    Examples:
        >>> transform = CenterCrop(640)
        >>> image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
        >>> cropped_image = transform(image)
        >>> print(cropped_image.shape)
        (640, 640, 3)
    '''

    def __init__(self, size: Union[int, Tuple[int, int]] = 640):
        '''
        Initializes the CenterCrop object for image preprocessing.
        This class is designed to be part of a transformation pipeline, e.g., T.Compose([CenterCrop(size), ToTensor()]).
        It performs a center crop on input images to a specified size.
        Args:
            size (int | Tuple[int, int]): The desired output size of the crop. If size is an int, a square crop
                (size, size) is made. If size is a sequence like (h, w), it is used as the output size.
        Returns:
            (None): This method initializes the object and does not return anything.
        Examples:
            >>> transform = CenterCrop(224)
            >>> img = np.random.rand(300, 300, 3)
            >>> cropped_img = transform(img)
            >>> print(cropped_img.shape)
            (224, 224, 3)
        '''
        if isinstance(size, int):
            self.h, self.w = size, size
        elif isinstance(size, (tuple, list)) and len(size) == 2:
            self.h, self.w = int(size[0]), int(size[1])
        else:
            raise ValueError("size must be an int or a tuple/list of (h, w)")
        if self.h <= 0 or self.w <= 0:
            raise ValueError("size dimensions must be positive integers")

    def __call__(self, im):
        '''
        Applies center cropping to an input image.
        This method resizes and crops the center of the image using a letterbox method. It maintains the aspect
        ratio of the original image while fitting it into the specified dimensions.
        Args:
            im (numpy.ndarray | PIL.Image.Image): The input image as a numpy array of shape (H, W, C) or a
                PIL Image object.
        Returns:
            (numpy.ndarray): The center-cropped and resized image as a numpy array of shape (self.h, self.w, C).
        Examples:
            >>> transform = CenterCrop(size=224)
            >>> image = np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8)
            >>> cropped_image = transform(image)
            >>> assert cropped_image.shape == (224, 224, 3)
        '''
        if isinstance(im, Image.Image):
            im = np.array(im)
        if not isinstance(im, np.ndarray):
            raise TypeError("Input must be a numpy.ndarray or PIL.Image.Image")

        if im.ndim not in (2, 3):
            raise ValueError("Input array must be HxW or HxWxC")

        h0, w0 = im.shape[:2]
        if h0 == 0 or w0 == 0:
            raise ValueError("Input image has invalid dimensions")

        scale = max(self.h / h0, self.w / w0)
        new_h = max(1, int(math.ceil(h0 * scale)))
        new_w = max(1, int(math.ceil(w0 * scale)))

        interp = cv2.INTER_AREA if scale < 1.0 else cv2.INTER_LINEAR
        resized = cv2.resize(im, (new_w, new_h), interpolation=interp)
        if im.ndim == 3 and resized.ndim == 2:
            resized = resized[:, :, np.newaxis]

        y0 = max(0, (new_h - self.h) // 2)
        x0 = max(0, (new_w - self.w) // 2)
        y1 = y0 + self.h
        x1 = x0 + self.w

        cropped = resized[y0:y1, x0:x1]
        if cropped.shape[0] != self.h or cropped.shape[1] != self.w:
            # Handle edge rounding cases to ensure exact output size
            cropped = cv2.resize(cropped, (self.w, self.h),
                                 interpolation=cv2.INTER_LINEAR)

        return cropped
