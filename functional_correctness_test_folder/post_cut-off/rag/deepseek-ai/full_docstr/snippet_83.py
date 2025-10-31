
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
            self.h = size
            self.w = size
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
        if isinstance(im, Image.Image):
            im = np.array(im)

        h, w = im.shape[:2]
        scale = min(self.h / h, self.w / w)
        new_h, new_w = int(h * scale), int(w * scale)

        # Resize the image
        if im.ndim == 3:
            im_resized = np.array(Image.fromarray(
                im).resize((new_w, new_h), Image.BILINEAR))
        else:
            im_resized = np.array(Image.fromarray(
                im).resize((new_w, new_h), Image.BILINEAR))

        # Center crop
        top = (self.h - new_h) // 2
        left = (self.w - new_w) // 2

        if im_resized.ndim == 3:
            padded = np.zeros(
                (self.h, self.w, im_resized.shape[2]), dtype=im_resized.dtype)
        else:
            padded = np.zeros((self.h, self.w), dtype=im_resized.dtype)

        padded[top:top + new_h, left:left + new_w] = im_resized
        return padded
