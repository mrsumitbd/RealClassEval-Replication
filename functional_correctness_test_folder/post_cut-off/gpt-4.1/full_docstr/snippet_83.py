
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
        elif isinstance(size, (tuple, list)) and len(size) == 2:
            self.h, self.w = int(size[0]), int(size[1])
        else:
            raise ValueError("size must be int or tuple/list of length 2")

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
            raise TypeError("Input must be a numpy array or PIL Image.")

        if im.ndim == 2:
            im = im[..., None]
        if im.ndim == 3 and im.shape[2] == 1:
            im = np.repeat(im, 3, axis=2)

        orig_h, orig_w = im.shape[:2]
        target_h, target_w = self.h, self.w

        # Compute scale to fit the image into the target size while maintaining aspect ratio
        scale = min(orig_h / target_h, orig_w / target_w)
        crop_h = int(round(target_h * scale))
        crop_w = int(round(target_w * scale))

        # Compute top-left corner of the crop
        y1 = max((orig_h - crop_h) // 2, 0)
        x1 = max((orig_w - crop_w) // 2, 0)
        y2 = y1 + crop_h
        x2 = x1 + crop_w

        # Crop the image
        cropped = im[y1:y2, x1:x2]

        # Resize to target size
        if cropped.shape[0] != target_h or cropped.shape[1] != target_w:
            # Use PIL for resizing to preserve quality
            pil_img = Image.fromarray(cropped)
            pil_img = pil_img.resize((target_w, target_h), Image.BILINEAR)
            cropped = np.array(pil_img)

        # Ensure output shape is (h, w, c)
        if cropped.ndim == 2:
            cropped = cropped[..., None]
        if cropped.shape[2] == 1:
            cropped = np.repeat(cropped, 3, axis=2)
        return cropped
