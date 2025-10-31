import math
from typing import Tuple

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

    def __init__(self, size=(640, 640), auto=False, stride=32):
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
                "size must be an int or a tuple/list of (height, width)")

        if h <= 0 or w <= 0:
            raise ValueError(
                "Target height and width must be positive integers")

        self.h = h
        self.w = w
        self.auto = bool(auto)
        self.stride = int(stride) if stride is not None else 32
        if self.stride <= 0:
            raise ValueError("stride must be a positive integer")

    def __call__(self, im):
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

        if im.ndim == 2:
            im = np.stack([im, im, im], axis=-1)
        elif im.ndim == 3:
            if im.shape[2] == 1:
                im = np.concatenate([im, im, im], axis=2)
            elif im.shape[2] >= 3:
                im = im[:, :, :3]
            else:
                raise ValueError(
                    "Input image must have 1 or at least 3 channels")
        else:
            raise ValueError("Input image must have shape (H, W) or (H, W, C)")

        ih, iw = int(im.shape[0]), int(im.shape[1])

        # Determine target dimensions, optionally aligned to stride
        th, tw = self.h, self.w
        if self.auto:
            th = int(math.ceil(th / self.stride) * self.stride)
            tw = int(math.ceil(tw / self.stride) * self.stride)

        # Compute resize ratio and new size
        r = min(th / ih, tw / iw)
        new_h = max(int(round(ih * r)), 1)
        new_w = max(int(round(iw * r)), 1)

        # Resize
        try:
            import cv2
            interp = cv2.INTER_LINEAR if im.dtype != np.uint8 else cv2.INTER_AREA if (
                new_h < ih or new_w < iw) else cv2.INTER_LINEAR
            resized = cv2.resize(im, (new_w, new_h), interpolation=interp)
        except Exception:
            # Fallback to PIL if OpenCV not available
            from PIL import Image
            pil_im = Image.fromarray(im)
            resized = np.array(pil_im.resize(
                (new_w, new_h), resample=Image.BILINEAR))

        # Compute padding (symmetric)
        pad_h = th - new_h
        pad_w = tw - new_w
        if pad_h < 0 or pad_w < 0:
            # In rare cases due to rounding, adjust by trimming resize by 1 pixel
            new_h = min(new_h, th)
            new_w = min(new_w, tw)
            try:
                import cv2
                resized = cv2.resize(
                    resized, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
            except Exception:
                from PIL import Image
                resized = np.array(Image.fromarray(resized).resize(
                    (new_w, new_h), resample=Image.BILINEAR))
            pad_h = th - new_h
            pad_w = tw - new_w

        top = pad_h // 2
        bottom = pad_h - top
        left = pad_w // 2
        right = pad_w - left

        # Determine padding value based on dtype
        if np.issubdtype(resized.dtype, np.integer):
            pad_val = [114, 114, 114]
        else:
            pad_val = [114.0 / 255.0, 114.0 / 255.0, 114.0 / 255.0]

        # Pad to target size
        try:
            import cv2
            out = cv2.copyMakeBorder(
                resized, top, bottom, left, right, borderType=cv2.BORDER_CONSTANT, value=pad_val)
        except Exception:
            out = np.pad(
                resized,
                ((top, bottom), (left, right), (0, 0)),
                mode="constant",
                constant_values=tuple((v, v) for v in pad_val),
            )

        return out
