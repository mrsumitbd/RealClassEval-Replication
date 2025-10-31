import numpy as np
import cv2


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
            self.h = int(size)
            self.w = int(size)
        elif isinstance(size, (tuple, list)) and len(size) == 2:
            self.h = int(size[0])
            self.w = int(size[1])
        else:
            raise ValueError(
                "size must be an int or a tuple/list of (height, width)")
        if self.h <= 0 or self.w <= 0:
            raise ValueError("Target size must be positive integers")
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
            im = im[..., None]
        if im.ndim != 3:
            raise ValueError("Input image must have shape (H, W, C)")

        # Ensure 3 channels (convert grayscale to 3 channels, drop alpha if present)
        if im.shape[2] == 1:
            im = np.repeat(im, 3, axis=2)
        elif im.shape[2] > 3:
            im = im[:, :, :3]

        h0, w0 = im.shape[:2]

        # Determine padding value based on dtype
        if np.issubdtype(im.dtype, np.integer):
            pad_value = 114
        else:
            pad_value = 114.0 / 255.0
        pad_color = (pad_value, pad_value, pad_value)

        # Compute scale using target short side; optionally align short side to a multiple of stride
        target_short = min(self.h, self.w)
        if self.auto and self.stride > 1:
            target_short = max(
                self.stride, (target_short // self.stride) * self.stride)

        r = target_short / min(h0, w0)
        # Ensure we don't exceed the target bounding box
        r = min(r, self.h / h0, self.w / w0)

        new_w = max(int(round(w0 * r)), 1)
        new_h = max(int(round(h0 * r)), 1)

        # Choose interpolation: downscale -> INTER_AREA, upscale -> INTER_LINEAR
        if r < 1.0:
            interp = cv2.INTER_AREA
        else:
            interp = cv2.INTER_LINEAR

        if (new_w, new_h) != (w0, h0):
            im = cv2.resize(im, (new_w, new_h), interpolation=interp)

        # Compute padding to reach target (centered)
        dw = self.w - new_w
        dh = self.h - new_h
        if dw < 0 or dh < 0:
            # Numerical safety: fallback to strict scaling by min ratio
            r = min(self.h / h0, self.w / w0)
            new_w = max(int(round(w0 * r)), 1)
            new_h = max(int(round(h0 * r)), 1)
            im = cv2.resize(im, (new_w, new_h), interpolation=interp)
            dw = self.w - new_w
            dh = self.h - new_h

        top = dh // 2
        bottom = dh - top
        left = dw // 2
        right = dw - left

        im = cv2.copyMakeBorder(
            im, top, bottom, left, right, borderType=cv2.BORDER_CONSTANT, value=pad_color)

        # Guarantee exact target shape and 3 channels
        if im.shape[0] != self.h or im.shape[1] != self.w:
            im = cv2.resize(im, (self.w, self.h),
                            interpolation=cv2.INTER_LINEAR)
        if im.shape[2] != 3:
            if im.shape[2] == 1:
                im = np.repeat(im, 3, axis=2)
            else:
                im = im[:, :, :3]

        return im
