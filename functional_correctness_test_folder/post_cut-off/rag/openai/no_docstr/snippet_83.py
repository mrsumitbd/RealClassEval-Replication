
import numpy as np
import cv2
from PIL import Image
from collections.abc import Sequence


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

    def __init__(self, size=640):
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
            self.h = self.w = size
        elif isinstance(size, Sequence) and len(size) == 2:
            self.h, self.w = size
        else:
            raise ValueError('size must be int or tuple of two ints')

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
        # Convert PIL to numpy if needed
        if isinstance(im, Image.Image):
            im = np.array(im)

        if im.ndim == 2:  # grayscale
            im = im[:, :, None]

        H, W = im.shape[:2]

        # Compute scale to fit the image inside target while preserving aspect ratio
        scale = min(self.w / W, self.h / H)
        new_W = int(round(W * scale))
        new_H = int(round(H * scale))

        # Resize
        resized = cv2.resize(im, (new_W, new_H),
                             interpolation=cv2.INTER_LINEAR)

        # Pad if necessary to reach target size (letterbox)
        pad_w = self.w - new_W
        pad_h = self.h - new_H
        top = pad_h // 2
        bottom = pad_h - top
        left = pad_w // 2
        right = pad_w - left
        if pad_w > 0 or pad_h > 0:
            resized = cv2.copyMakeBorder(resized, top, bottom, left, right,
                                         borderType=cv2.BORDER_CONSTANT, value=0)

        # If after padding we still have larger dimensions (due to rounding), crop center
        final_H, final_W = resized.shape[:2]
        start_y = (final_H - self.h) // 2
        start_x = (final_W - self.w) // 2
        cropped = resized[start_y:start_y + self.h, start_x:start_x + self.w]

        return cropped
