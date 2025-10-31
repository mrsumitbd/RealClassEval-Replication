import numpy as np
from typing import Tuple, Union


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

    def __init__(self, size: Union[int, Tuple[int, int]] = 640):
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
            self.h = int(size)
            self.w = int(size)
        elif isinstance(size, (tuple, list)) and len(size) == 2:
            self.h = int(size[0])
            self.w = int(size[1])
        else:
            raise ValueError("size must be an int or a tuple/list of length 2")
        if self.h <= 0 or self.w <= 0:
            raise ValueError("size dimensions must be positive integers")

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
        try:
            from PIL import Image  # noqa: F401
            PIL_AVAILABLE = True
        except Exception:
            PIL_AVAILABLE = False

        if PIL_AVAILABLE:
            from PIL.Image import Image as PILImage
            if isinstance(im, PILImage):
                im = np.array(im)

        if not isinstance(im, np.ndarray):
            raise TypeError(
                "Input must be a numpy.ndarray or a PIL.Image.Image")

        # Ensure shape is HxWxC
        if im.ndim == 2:
            im = im[..., None]
        elif im.ndim == 3:
            pass
        else:
            raise ValueError(
                "Input numpy array must have shape (H, W) or (H, W, C)")

        H, W, C = im.shape
        target_h, target_w = self.h, self.w

        # Scale to cover target, then center crop to target size
        scale = max(target_h / max(H, 1), target_w / max(W, 1))

        new_h = max(1, int(round(H * scale)))
        new_w = max(1, int(round(W * scale)))

        def resize_nn(arr: np.ndarray, out_h: int, out_w: int) -> np.ndarray:
            in_h, in_w = arr.shape[:2]
            # Compute indices with floor mapping
            ys = np.minimum((np.arange(out_h) * in_h // out_h),
                            in_h - 1).astype(np.int64)
            xs = np.minimum((np.arange(out_w) * in_w // out_w),
                            in_w - 1).astype(np.int64)
            if arr.ndim == 3:
                return arr[ys[:, None], xs[None, :], :]
            else:
                return arr[ys[:, None], xs[None, :]]

        resized = resize_nn(im, new_h, new_w)

        # Center crop
        start_y = max(0, (new_h - target_h) // 2)
        start_x = max(0, (new_w - target_w) // 2)
        end_y = start_y + target_h
        end_x = start_x + target_w

        # If resized is smaller due to rounding, pad before crop
        pad_top = max(0, -start_y)
        pad_left = max(0, -start_x)
        pad_bottom = max(0, end_y - resized.shape[0])
        pad_right = max(0, end_x - resized.shape[1])

        if any(v > 0 for v in (pad_top, pad_bottom, pad_left, pad_right)):
            pad_width = ((pad_top, pad_bottom), (pad_left, pad_right), (0, 0))
            # Use edge padding to avoid introducing new colors
            resized = np.pad(resized, pad_width=pad_width, mode='edge')
            new_h, new_w = resized.shape[:2]
            start_y = max(0, (new_h - target_h) // 2)
            start_x = max(0, (new_w - target_w) // 2)
            end_y = start_y + target_h
            end_x = start_x + target_w

        cropped = resized[start_y:end_y, start_x:end_x, :]

        # Ensure output shape
        if cropped.shape[0] != target_h or cropped.shape[1] != target_w:
            # As a fallback, resize to exact target in case of any off-by-one
            cropped = resize_nn(cropped, target_h, target_w)

        return cropped
