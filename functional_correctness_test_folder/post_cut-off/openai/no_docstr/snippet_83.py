
import numpy as np
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
        else:
            self.h, self.w = size

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
        if isinstance(im, Image.Image):
            im = np.array(im)

        if not isinstance(im, np.ndarray):
            raise TypeError('Input must be a numpy array or PIL Image')

        h_in, w_in = im.shape[:2]

        # Compute top-left corner of crop
        top = max((h_in - self.h) // 2, 0)
        left = max((w_in - self.w) // 2, 0)

        # If the image is smaller than the target, pad with zeros
        if h_in < self.h or w_in < self.w:
            # Create a black canvas
            canvas = np.zeros((self.h, self.w, im.shape[2]), dtype=im.dtype)
            # Compute where to place the original image
            top_pad = (self.h - h_in) // 2
            left_pad = (self.w - w_in) // 2
            canvas[top_pad:top_pad + h_in, left_pad:left_pad + w_in] = im
            return canvas

        # Crop the image
        cropped = im[top:top + self.h, left:left + self.w]
        return cropped
