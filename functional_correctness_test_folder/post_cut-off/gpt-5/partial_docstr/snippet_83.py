import math
from typing import Tuple, Union

import numpy as np

try:
    from PIL import Image
except Exception as e:
    Image = None


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
            h, w = size, size
        elif isinstance(size, (tuple, list)) and len(size) == 2:
            h, w = int(size[0]), int(size[1])
        else:
            raise ValueError(
                "size must be an int or a tuple/list of two ints (h, w)")
        if h <= 0 or w <= 0:
            raise ValueError("size dimensions must be positive integers")
        self.h = int(h)
        self.w = int(w)

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
        if Image is None:
            raise RuntimeError(
                "PIL is required for CenterCrop but is not available.")

        # Convert input to PIL Image
        if isinstance(im, Image.Image):
            pil_im = im
        elif isinstance(im, np.ndarray):
            if im.ndim not in (2, 3):
                raise ValueError(
                    "Input numpy array must be 2D (H, W) or 3D (H, W, C)")
            # Ensure contiguous array for fromarray
            pil_im = Image.fromarray(np.ascontiguousarray(im))
        else:
            raise TypeError("Input must be a numpy.ndarray or PIL.Image.Image")

        # Get original dimensions
        orig_w, orig_h = pil_im.size  # PIL uses (W, H)

        # Compute scale to ensure both dims >= target dims
        scale = max(self.h / orig_h, self.w / orig_w)
        new_w = int(math.ceil(orig_w * scale))
        new_h = int(math.ceil(orig_h * scale))

        # Choose interpolation
        if pil_im.mode in ("1", "P"):
            resample = Image.NEAREST
        else:
            resample = Image.BILINEAR

        # Resize while keeping aspect ratio
        if (new_w, new_h) != (orig_w, orig_h):
            pil_im = pil_im.resize((new_w, new_h), resample=resample)

        # Compute centered crop box
        left = max((new_w - self.w) // 2, 0)
        top = max((new_h - self.h) // 2, 0)
        right = left + self.w
        bottom = top + self.h

        pil_im = pil_im.crop((left, top, right, bottom))

        # Convert back to numpy array
        out = np.array(pil_im)

        # Ensure shape consistency for grayscale to be (H, W) not (H, W, 1)
        if out.ndim == 2:
            return out
        return out
