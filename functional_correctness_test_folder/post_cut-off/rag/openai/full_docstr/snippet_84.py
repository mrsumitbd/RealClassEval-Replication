
import numpy as np
from PIL import Image


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
            h = w = size
        else:
            h, w = size
        if auto:
            h = int(round(h / stride) * stride)
            w = int(round(w / stride) * stride)
        self.h = h
        self.w = w
        self.auto = auto
        self.stride = stride

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
            raise TypeError(
                f'Input image must be a numpy.ndarray, got {type(im)}')
        if im.ndim != 3 or im.shape[2] not in (1, 3):
            raise ValueError(
                f'Input image must have shape (H, W, C) with C=1 or 3, got {im.shape}')

        h0, w0 = im.shape[:2]
        scale = min(self.h / h0, self.w / w0)
        new_h = int(round(h0 * scale))
        new_w = int(round(w0 * scale))

        # Resize image
        img_resized = Image.fromarray(im)
        img_resized = img_resized.resize((new_w, new_h), Image.BILINEAR)
        img_resized = np.array(img_resized)

        # Pad to target size
        pad_h = self.h - new_h
        pad_w = self.w - new_w
        top = pad_h // 2
        bottom = pad_h - top
        left = pad_w // 2
        right = pad_w - left

        # Use gray padding (128)
        padded = np.full((self.h, self.w, 3), 128, dtype=im.dtype)
        padded[top:top + new_h, left:left + new_w] = img_resized

        return padded
