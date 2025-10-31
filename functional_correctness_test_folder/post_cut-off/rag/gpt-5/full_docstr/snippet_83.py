import numpy as np
import cv2
from typing import Tuple, Union


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
            raise ValueError(
                "size must be an int or a tuple/list of two ints (h, w).")

        if self.h <= 0 or self.w <= 0:
            raise ValueError("size values must be positive integers.")

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
        # Convert PIL Image to numpy array if needed
        try:
            from PIL import Image
            if hasattr(im, "size") and callable(getattr(im, "resize", None)) and isinstance(im, Image.Image):
                im = np.array(im)
        except Exception:
            pass

        if not isinstance(im, np.ndarray):
            raise TypeError(
                "Input must be a numpy.ndarray or a PIL.Image.Image.")

        if im.ndim not in (2, 3):
            raise ValueError(
                "Input numpy array must have 2 (H, W) or 3 (H, W, C) dimensions.")

        orig_h, orig_w = im.shape[:2]
        if orig_h == 0 or orig_w == 0:
            raise ValueError("Input image has invalid dimensions.")

        # Compute scale to ensure the resized image fully covers the target crop (no padding), then center crop.
        scale = max(self.h / orig_h, self.w / orig_w)
        new_h = max(1, int(round(orig_h * scale)))
        new_w = max(1, int(round(orig_w * scale)))

        # Choose interpolation based on scaling direction
        if scale > 1.0:
            interp = cv2.INTER_LINEAR
        else:
            interp = cv2.INTER_AREA

        # Resize
        resized = cv2.resize(im, (new_w, new_h), interpolation=interp)

        # Compute center crop coordinates
        y1 = max((new_h - self.h) // 2, 0)
        x1 = max((new_w - self.w) // 2, 0)
        y2 = min(y1 + self.h, new_h)
        x2 = min(x1 + self.w, new_w)

        cropped = resized[y1:y2, x1:x2]

        # In rare rounding cases, pad to ensure exact size
        out_h, out_w = cropped.shape[:2]
        if (out_h, out_w) != (self.h, self.w):
            pad_top = (self.h - out_h) // 2
            pad_bottom = self.h - out_h - pad_top
            pad_left = (self.w - out_w) // 2
            pad_right = self.w - out_w - pad_left

            if cropped.ndim == 3:
                pad_width = ((pad_top, pad_bottom),
                             (pad_left, pad_right), (0, 0))
            else:
                pad_width = ((pad_top, pad_bottom), (pad_left, pad_right))

            cropped = np.pad(cropped, pad_width=pad_width,
                             mode="constant", constant_values=0)

        return cropped
