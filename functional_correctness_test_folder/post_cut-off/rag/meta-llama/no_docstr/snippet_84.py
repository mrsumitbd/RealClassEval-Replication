
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
        self.h, self.w = (size, size) if isinstance(size, int) else size
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
        # Resize image to fit within the specified dimensions while maintaining its aspect ratio
        h, w = im.shape[:2]
        scale = min(self.h / h, self.w / w)
        if self.auto:
            scale = min(self.h / h, self.w / w)
            new_h, new_w = int(round(h * scale)), int(round(w * scale))
            new_h = (new_h + self.stride - 1) // self.stride * self.stride
            new_w = (new_w + self.stride - 1) // self.stride * self.stride
        else:
            new_h, new_w = int(round(h * scale)), int(round(w * scale))

        # Pad the resized image to match the target size
        top = (self.h - new_h) // 2
        bottom = self.h - new_h - top
        left = (self.w - new_w) // 2
        right = self.w - new_w - left

        img = np.copy(im)
        img = np.asarray(np.dstack((np.rot90(img, 0), np.rot90(
            img, 0), np.rot90(img, 0))), dtype=np.uint8)
        resized_img = np.zeros((self.h, self.w, 3), dtype=np.uint8)

        resized_img = np.ascontiguousarray(resized_img.transpose((2, 0, 1)))
        img = np.ascontiguousarray(img.transpose((2, 0, 1)))

        resized = np.zeros((3, self.h, self.w), dtype=img.dtype)
        resized[:, top:top + new_h, left:left +
                new_w] = np.resize(img, (3, new_h, new_w))

        return np.ascontiguousarray(resized.transpose((1, 2, 0)))
