
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

        # Ensure image has 3 dimensions (H, W, C)
        if im.ndim == 2:  # grayscale
            im = im[:, :, None]
        elif im.ndim == 3 and im.shape[2] not in (1, 3, 4):
            raise ValueError('Unsupported image shape: {}'.format(im.shape))

        h_in, w_in = im.shape[:2]

        # Compute scale to fit target size while preserving aspect ratio
        scale = min(self.w / w_in, self.h / h_in)
        new_w = int(round(w_in * scale))
        new_h = int(round(h_in * scale))

        # Resize using PIL for better quality
        pil_im = Image.fromarray(im)
        pil_resized = pil_im.resize((new_w, new_h), Image.BILINEAR)
        resized = np.array(pil_resized)

        # Pad if resized image is smaller than target
        pad_h = max(self.h - new_h, 0)
        pad_w = max(self.w - new_w, 0)
        if pad_h > 0 or pad_w > 0:
            pad_top = pad_h // 2
            pad_bottom = pad_h - pad_top
            pad_left = pad_w // 2
            pad_right = pad_w - pad_left
            resized = np.pad(
                resized,
                ((pad_top, pad_bottom), (pad_left, pad_right), (0, 0)),
                mode='constant',
                constant_values=0
            )

        # Center crop to target size
        h_final, w_final = resized.shape[:2]
        start_h = (h_final - self.h) // 2
        start_w = (w_final - self.w) // 2
        cropped = resized[start_h:start_h + self.h, start_w:start_w + self.w]

        return cropped
