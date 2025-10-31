import numpy as np
from PIL import Image
import torch


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
        # Handle torch tensor input
        if isinstance(im, torch.Tensor):
            t = im
            if t.ndim == 3 and t.shape[0] != 3 and t.shape[-1] == 3:
                t = t.permute(2, 0, 1)
            if t.dtype.is_floating_point:
                t = t.clamp(0, 1)
            else:
                t = t.to(torch.float32).div_(255.0)
            if self.half:
                t = t.half()
            return t.contiguous()

        # Handle PIL Image input (assumed RGB)
        if isinstance(im, Image.Image):
            im = im.convert('RGB')
            im = np.array(im, copy=False)

        if not isinstance(im, np.ndarray):
            raise TypeError(
                f"Unsupported input type: {type(im)}. Expected numpy array, PIL Image, or torch Tensor.")

        # Ensure HWC
        if im.ndim == 2:
            im = im[..., None]  # H W 1

        # If more than 3 channels, drop alpha
        if im.ndim == 3 and im.shape[2] > 3:
            im = im[:, :, :3]

        # Determine if input was PIL (RGB) or numpy (assume BGR). We reversed only for numpy arrays.
        # Since PIL case has been converted to np already in RGB, detect by flag.
        # Simple heuristic: If the array was obtained here via PIL, it's uint8 RGB already.
        # We can't reliably detect origin, so assume BGR for numpy inputs and convert to RGB.
        # If user passed numpy RGB, this will swap to BGR->RGB anyway; spec expects BGR->RGB.
        # Convert BGR to RGB if 3-channel
        if im.shape[-1] == 3:
            im = im[..., ::-1]

        # Convert to CHW
        im = im.transpose(2, 0, 1).copy()

        # Convert to torch tensor
        t = torch.from_numpy(im)

        # Normalize to [0,1]
        if t.dtype == torch.uint8:
            t = t.to(torch.float32).div_(255.0)
        elif t.dtype == torch.uint16:
            t = t.to(torch.float32).div_(65535.0)
        elif t.dtype.is_floating_point:
            # Assume already in [0,1]; if not, user should normalize before.
            if t.dtype != torch.float32:
                t = t.to(torch.float32)
        else:
            # Other integer types
            t = t.to(torch.float32)
            max_val = float(t.max().item()) if t.numel() else 1.0
            if max_val > 0:
                t = t / max_val

        if self.half:
            t = t.half()

        return t.contiguous()
