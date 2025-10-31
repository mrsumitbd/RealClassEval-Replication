import numpy as np
import torch

try:
    from PIL import Image as PILImage
except Exception:  # PIL optional
    PILImage = None


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
        # Handle PIL Images by converting to numpy (assumed RGB)
        if PILImage is not None and isinstance(im, PILImage.Image):
            im = np.array(im)  # RGB
            pil_source = True
        else:
            pil_source = False

        # Handle torch tensors by converting to numpy first
        if isinstance(im, torch.Tensor):
            arr = im.detach().cpu().numpy()
        else:
            arr = im

        if not isinstance(arr, np.ndarray):
            raise TypeError(
                "Input must be a numpy array, PIL Image, or torch Tensor.")

        # Ensure at least 2D
        if arr.ndim == 2:
            arr = arr[..., None]  # H, W, 1

        if arr.ndim != 3:
            raise ValueError(
                f"Expected image with 3 dimensions (H, W, C), got shape {arr.shape}.")

        H, W, C = arr.shape
        if C not in (1, 3, 4):
            raise ValueError(f"Expected channels to be 1, 3, or 4, got {C}.")

        # If 4 channels, drop alpha
        if C == 4:
            arr = arr[..., :3]
            C = 3

        # Convert color: for numpy inputs (assumed BGR), convert to RGB; for PIL input (RGB), keep as is
        if C == 3 and not pil_source:
            arr = arr[..., ::-1]  # BGR to RGB

        # Convert to float
        dtype = torch.float16 if self.half else torch.float32

        # Decide normalization: if integer types or values clearly >1, divide by 255
        if np.issubdtype(arr.dtype, np.integer):
            arr = arr.astype(np.float32, copy=False)
            arr /= 255.0
        else:
            arr = arr.astype(np.float32, copy=False)
            # Normalize if values look like 0-255
            if np.nanmax(arr) > 1.0:
                arr /= 255.0

        # HWC -> CHW and contiguous
        arr = np.ascontiguousarray(np.transpose(arr, (2, 0, 1)))

        tensor = torch.from_numpy(arr).to(dtype)
        return tensor
