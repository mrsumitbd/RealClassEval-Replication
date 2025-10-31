import numpy as np
import torch

try:
    from PIL import Image as _PILImage
except Exception:  # PIL may not be installed
    _PILImage = None


class ToTensor:
    '''
    Converts an image from a numpy array to a PyTorch tensor.
    This class is designed to be part of a transformation pipeline, e.g., T.Compose([LetterBox(size), ToTensor()]).
    Attributes:
        half (bool): If True, converts the image to half precision (float16).
    Methods:
        __call__: Applies the tensor conversion to an input image.
    Examples:
        >>> transform = ToTensor(half=True)
        >>> img = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
        >>> tensor_img = transform(img)
        >>> print(tensor_img.shape, tensor_img.dtype)
        torch.Size([3, 640, 640]) torch.float16
    Notes:
        The input image is expected to be in BGR format with shape (H, W, C).
        The output tensor will be in RGB format with shape (C, H, W), normalized to [0, 1].
    '''

    def __init__(self, half=False):
        '''
        Initializes the ToTensor object for converting images to PyTorch tensors.
        This class is designed to be used as part of a transformation pipeline for image preprocessing in the
        Ultralytics YOLO framework. It converts numpy arrays or PIL Images to PyTorch tensors, with an option
        for half-precision (float16) conversion.
        Args:
            half (bool): If True, converts the tensor to half precision (float16). Default is False.
        Examples:
            >>> transform = ToTensor(half=True)
            >>> img = np.random.rand(640, 640, 3)
            >>> tensor_img = transform(img)
            >>> print(tensor_img.dtype)
            torch.float16
        '''
        self.half = bool(half)

    def __call__(self, im):
        '''
        Transforms an image from a numpy array to a PyTorch tensor.
        This method converts the input image from a numpy array to a PyTorch tensor, applying optional
        half-precision conversion and normalization. The image is transposed from HWC to CHW format and
        the color channels are reversed from BGR to RGB.
        Args:
            im (numpy.ndarray): Input image as a numpy array with shape (H, W, C) in BGR order.
        Returns:
            (torch.Tensor): The transformed image as a PyTorch tensor in float32 or float16, normalized
                to [0, 1] with shape (C, H, W) in RGB order.
        Examples:
            >>> transform = ToTensor(half=True)
            >>> img = np.random.randint(0, 255, (640, 640, 3), dtype=np.uint8)
            >>> tensor_img = transform(img)
            >>> print(tensor_img.shape, tensor_img.dtype)
            torch.Size([3, 640, 640]) torch.float16
        '''
        from_pil = False

        if _PILImage is not None and isinstance(im, _PILImage):
            im = np.asarray(im)  # PIL provides RGB by default
            from_pil = True

        if not isinstance(im, np.ndarray):
            raise TypeError(
                f'Expected input as numpy.ndarray or PIL.Image, but got {type(im)}')

        im = np.ascontiguousarray(im)

        if im.ndim == 2:
            im = im[..., None]

        if im.ndim != 3:
            raise ValueError(
                f'Expected image with 3 dimensions (H, W, C), but got shape {im.shape}')

        # Drop alpha channel if present
        if im.shape[2] > 3:
            im = im[..., :3]

        # Convert BGR to RGB unless image came from PIL (already RGB)
        if not from_pil and im.shape[2] == 3:
            im = im[..., ::-1]

        # Determine if normalization by 255 is needed
        kind = im.dtype.kind
        if kind in ('u', 'i'):  # unsigned/signed integers
            needs_scale = True
        elif kind == 'f':
            # If float and values exceed 1.0, assume 0-255 range and scale
            needs_scale = float(np.max(im)) > 1.0
        elif kind == 'b':  # boolean
            needs_scale = False
        else:
            # Fallback: treat as integers
            needs_scale = True

        tensor = torch.from_numpy(im.transpose(2, 0, 1)).contiguous()

        dtype = torch.float16 if self.half else torch.float32
        tensor = tensor.to(dtype=dtype)

        if needs_scale:
            tensor = tensor.div_(255.0)

        return tensor
