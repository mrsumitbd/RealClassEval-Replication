
import numpy as np
from PIL import Image
import cv2


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

        # Ensure im is a numpy array
        if not isinstance(im, np.ndarray):
            raise TypeError(f'Unsupported image type: {type(im)}')

        # Handle grayscale images by adding a channel dimension
        if im.ndim == 2:
            im = im[:, :, None]

        h_in, w_in = im.shape[:2]

        # If the input image is smaller than the target, resize directly
        if h_in < self.h or w_in < self.w:
            resized = cv2.resize(im, (self.w, self.h),
                                 interpolation=cv2.INTER_LINEAR)
            return resized

        # Compute coordinates for center crop
        start_y = (h_in - self.h) // 2
        start_x = (w_in - self.w) // 2

        cropped = im[start_y:start_y + self.h, start_x:start_x + self.w]
        return cropped
