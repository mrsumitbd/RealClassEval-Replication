
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
            try:
                h, w = size
            except Exception:
                raise ValueError('size must be int or tuple of two ints')
            self.h, self.w = int(h), int(w)

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

        orig_h, orig_w = im.shape[:2]

        # Compute scaling factor to fit inside target while preserving aspect ratio
        scale = min(self.w / orig_w, self.h / orig_h)

        new_w = int(round(orig_w * scale))
        new_h = int(round(orig_h * scale))

        # Resize
        resized = cv2.resize(im, (new_w, new_h),
                             interpolation=cv2.INTER_LINEAR)

        # Pad if necessary to reach target size (letterbox)
        pad_w = self.w - new_w
        pad_h = self.h - new_h
        top = pad_h // 2
        bottom = pad_h - top
        left = pad_w // 2
        right = pad_w - left

        if pad_w > 0 or pad_h > 0:
            # Use constant border (black)
            resized = cv2.copyMakeBorder(resized, top, bottom, left, right,
                                         borderType=cv2.BORDER_CONSTANT, value=0)

        # If after padding we still don't have exact size (due to rounding), crop to target
        final_h, final_w = resized.shape[:2]
        if final_h != self.h or final_w != self.w:
            start_y = (final_h - self.h) // 2
            start_x = (final_w - self.w) // 2
            resized = resized[start_y:start_y +
                              self.h, start_x:start_x + self.w]

        # Remove channel dim if original was grayscale
        if im.ndim == 2 and resized.ndim == 3 and resized.shape[2] == 1:
            resized = resized[:, :, 0]

        return resized
