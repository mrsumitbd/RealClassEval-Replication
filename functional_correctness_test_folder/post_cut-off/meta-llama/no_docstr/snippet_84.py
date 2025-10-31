
import numpy as np
from typing import Tuple, Union


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
            size = (size, size)
        self.h, self.w = size
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
        # Get the original height and width of the image
        h, w = im.shape[:2]

        # Calculate the ratio for resizing
        r = min(self.h / h, self.w / w)

        # If auto is True, adjust the target size based on stride
        if self.auto:
            new_h, new_w = self.h, self.w
            new_h = int(np.ceil(new_h / self.stride) * self.stride)
            new_w = int(np.ceil(new_w / self.stride) * self.stride)
            r = min(new_h / h, new_w / w)
            self.h, self.w = new_h, new_w

        # Calculate the new dimensions after resizing
        new_unpad = int(round(w * r)), int(round(h * r))
        dw, dh = self.w - new_unpad[0], self.h - new_unpad[1]

        # Resize the image
        im = np.array(im, dtype=np.float32)  # Ensure im is float32
        resized_im = np.zeros((self.h, self.w, im.shape[2]), dtype=im.dtype)
        resized_im.fill(114)  # Default padding value

        # Calculate the top and left padding
        dw, dh = dw / 2, dh / 2
        top, left = int(round(dh - 0.1)), int(round(dw - 0.1))
        resized = np.resize(
            im, (int(round(h * r)), int(round(w * r)), im.shape[2]))

        # Paste the resized image into the padded image
        resized_im[top:top + resized.shape[0],
                   left:left + resized.shape[1], :] = resized

        return resized_im.astype(np.uint8)
