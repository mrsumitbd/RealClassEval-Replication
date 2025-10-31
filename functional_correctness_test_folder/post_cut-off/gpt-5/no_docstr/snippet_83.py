import numpy as np
from PIL import Image
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
            self.h = size
            self.w = size
        else:
            if (
                not isinstance(size, (tuple, list))
                or len(size) != 2
                or not all(isinstance(x, int) for x in size)
            ):
                raise ValueError(
                    "size must be an int or a tuple/list of two ints (h, w)")
            self.h, self.w = int(size[0]), int(size[1])
        if self.h <= 0 or self.w <= 0:
            raise ValueError("size values must be positive integers")

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
            arr = np.array(im)
        elif isinstance(im, np.ndarray):
            arr = im
        else:
            raise TypeError("Input must be a numpy.ndarray or PIL.Image.Image")

        if arr.ndim == 2:
            # Grayscale, add channel dim for consistent processing then remove at the end
            arr = arr[:, :, None]
            grayscale = True
        elif arr.ndim == 3:
            grayscale = False
        else:
            raise ValueError(
                "Input array must have 2 (H, W) or 3 (H, W, C) dimensions")

        in_h, in_w = arr.shape[:2]

        # Compute scale to ensure resized image is at least as large as target in both dimensions
        scale = max(self.h / in_h, self.w / in_w)
        new_h = max(1, int(round(in_h * scale)))
        new_w = max(1, int(round(in_w * scale)))

        # Resize maintaining aspect ratio
        if new_h != in_h or new_w != in_w:
            arr_resized = self._resize_array(arr, (new_h, new_w))
        else:
            arr_resized = arr

        # Center crop to target size
        top = max(0, (arr_resized.shape[0] - self.h) // 2)
        left = max(0, (arr_resized.shape[1] - self.w) // 2)
        bottom = top + self.h
        right = left + self.w

        # Safety in case of rounding causing off-by-one
        top = max(0, min(top, arr_resized.shape[0] - self.h))
        left = max(0, min(left, arr_resized.shape[1] - self.w))

        cropped = arr_resized[top:bottom, left:right, :]

        if grayscale:
            cropped = cropped[:, :, 0]

        return cropped

    @staticmethod
    def _resize_array(arr: np.ndarray, new_hw: Tuple[int, int]) -> np.ndarray:
        new_h, new_w = new_hw
        resample = Image.BILINEAR

        c = arr.shape[2]
        dtype = arr.dtype

        # Try fast path for common cases with uint8 and 1/3/4 channels
        if dtype == np.uint8 and c in (1, 3, 4):
            if c == 1:
                img = Image.fromarray(arr[:, :, 0], mode="L")
                img = img.resize((new_w, new_h), resample=resample)
                out = np.array(img)[:, :, None]
            elif c == 3:
                img = Image.fromarray(arr, mode="RGB")
                img = img.resize((new_w, new_h), resample=resample)
                out = np.array(img)
            else:  # c == 4
                img = Image.fromarray(arr, mode="RGBA")
                img = img.resize((new_w, new_h), resample=resample)
                out = np.array(img)
            if out.ndim == 2:
                out = out[:, :, None]
            return out

        # Fallback: resize each channel independently to support arbitrary dtypes/channel counts
        channels = []
        for ch in range(c):
            ch_arr = arr[:, :, ch]
            # Convert to PIL Image; for non-uint8 types, PIL will use mode 'F' as needed
            ch_img = Image.fromarray(ch_arr)
            ch_img = ch_img.resize((new_w, new_h), resample=resample)
            ch_resized = np.array(ch_img)
            channels.append(ch_resized)
        out = np.stack(channels, axis=2)

        # Ensure dtype consistency if possible
        if out.dtype != dtype:
            try:
                out = out.astype(dtype, copy=False)
            except Exception:
                pass

        return out
