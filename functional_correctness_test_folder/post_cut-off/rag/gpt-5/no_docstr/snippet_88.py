import numpy as np
import torch

try:
    from PIL import Image
except Exception:  # PIL may not be available
    Image = None


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
        if Image is not None and isinstance(im, Image.Image):
            arr = np.asarray(im)
            if arr.ndim == 2:
                arr = arr[:, :, None]
            # PIL gives RGB. Keep as is.
        elif isinstance(im, np.ndarray):
            arr = im
            if arr.ndim == 2:
                arr = arr[:, :, None]
            c = arr.shape[2]
            if c == 3:
                # BGR -> RGB
                arr = arr[..., ::-1]
            elif c == 4:
                # BGRA -> RGBA
                b, g, r, a = np.split(arr, 4, axis=2)
                arr = np.concatenate((r, g, b, a), axis=2)
        elif isinstance(im, torch.Tensor):
            t = im
            # If HWC, convert to CHW
            if t.ndim == 3 and t.shape[0] not in (1, 3, 4):
                t = t.permute(2, 0, 1).contiguous()
            # Normalize
            if not torch.is_floating_point(t):
                t = t.to(torch.float32)
                if t.max() > 1:
                    t = t / 255.0
            else:
                if t.dtype != torch.float32 and not self.half:
                    t = t.to(torch.float32)
                if t.max() > 1:
                    t = t / 255.0
            if self.half:
                t = t.half()
            return t
        else:
            raise TypeError(
                "Input must be a numpy.ndarray, PIL.Image.Image, or torch.Tensor")

        chw = np.transpose(arr, (2, 0, 1))
        chw = np.ascontiguousarray(chw)
        t = torch.from_numpy(chw)

        if t.dtype == torch.uint8:
            t = t.to(torch.float32).div_(255.0)
        elif t.dtype in (torch.int8, torch.int16, torch.int32, torch.int64, torch.uint16, torch.uint32):
            t = t.to(torch.float32)
            if t.max() > 1:
                t = t / 255.0
        else:
            # float types
            if t.dtype != torch.float32 and not self.half:
                t = t.to(torch.float32)
            if torch.is_floating_point(t) and t.max() > 1:
                t = t / 255.0

        if self.half:
            t = t.half()

        return t
