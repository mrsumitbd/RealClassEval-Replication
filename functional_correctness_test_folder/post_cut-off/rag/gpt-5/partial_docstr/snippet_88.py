import numpy as np
import torch
from PIL import Image


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
        # Handle already-tensor inputs (optional convenience)
        if isinstance(im, torch.Tensor):
            if im.ndim != 3 or im.shape[0] not in (1, 3):
                raise TypeError("Expected a CHW torch.Tensor with C=1 or 3.")
            dtype = torch.float16 if self.half else torch.float32
            im = im.to(dtype)
            if im.max() > 1:
                im = im / 255.0
            return im

        input_is_bgr = True

        if isinstance(im, Image.Image):
            if im.mode != 'RGB':
                im = im.convert('RGB')
            im = np.asarray(im)
            input_is_bgr = False
        elif not isinstance(im, np.ndarray):
            raise TypeError("Input must be a numpy.ndarray or PIL.Image.Image")

        if im.ndim == 2:
            im = im[..., None]

        if im.shape[-1] == 4:
            im = im[..., :3]

        if im.shape[-1] != 3:
            raise ValueError(
                f"Expected image with 3 channels, got shape {im.shape}")

        if input_is_bgr:
            im = im[..., ::-1]  # BGR -> RGB

        im = im.transpose(2, 0, 1)  # HWC -> CHW
        im = np.ascontiguousarray(im)
        im_max = float(im.max()) if im.size > 0 else 0.0

        tensor = torch.from_numpy(im)

        target_dtype = torch.float16 if self.half else torch.float32
        if tensor.dtype.is_floating_point:
            tensor = tensor.to(target_dtype)
            if im_max > 1.0:
                tensor = tensor / 255.0
        else:
            tensor = tensor.to(target_dtype).div_(255.0)

        return tensor
