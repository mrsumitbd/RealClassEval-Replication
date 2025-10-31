
import torch
import numpy as np


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
        self.half = half

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
        if len(im.shape) < 3:
            im = np.expand_dims(im, -1)
        im = np.ascontiguousarray(im.transpose(
            (2, 0, 1))[::-1])  # HWC to CHW, BGR to RGB
        im = torch.from_numpy(im)
        im = im.float()  # uint8 to float32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if self.half:
            im = im.half()
        return im
