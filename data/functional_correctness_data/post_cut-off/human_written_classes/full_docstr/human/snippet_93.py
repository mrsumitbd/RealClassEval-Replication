import torch
from ultralytics.utils import IS_COLAB, IS_KAGGLE, LOGGER, ops

class LoadTensor:
    """
    A class for loading and processing tensor data for object detection tasks.

    This class handles the loading and pre-processing of image data from PyTorch tensors, preparing them for
    further processing in object detection pipelines.

    Attributes:
        im0 (torch.Tensor): The input tensor containing the image(s) with shape (B, C, H, W).
        bs (int): Batch size, inferred from the shape of `im0`.
        mode (str): Current processing mode, set to 'image'.
        paths (List[str]): List of image paths or auto-generated filenames.

    Methods:
        _single_check: Validates and formats an input tensor.

    Examples:
        >>> import torch
        >>> tensor = torch.rand(1, 3, 640, 640)
        >>> loader = LoadTensor(tensor)
        >>> paths, images, info = next(iter(loader))
        >>> print(f"Processed {len(images)} images")
    """

    def __init__(self, im0) -> None:
        """Initialize LoadTensor object for processing torch.Tensor image data."""
        self.im0 = self._single_check(im0)
        self.bs = self.im0.shape[0]
        self.mode = 'image'
        self.paths = [getattr(im, 'filename', f'image{i}.jpg') for i, im in enumerate(im0)]

    @staticmethod
    def _single_check(im, stride=32):
        """Validates and formats a single image tensor, ensuring correct shape and normalization."""
        s = f'WARNING ⚠️ torch.Tensor inputs should be BCHW i.e. shape(1, 3, 640, 640) divisible by stride {stride}. Input shape{tuple(im.shape)} is incompatible.'
        if len(im.shape) != 4:
            if len(im.shape) != 3:
                raise ValueError(s)
            LOGGER.warning(s)
            im = im.unsqueeze(0)
        if im.shape[2] % stride or im.shape[3] % stride:
            raise ValueError(s)
        if im.max() > 1.0 + torch.finfo(im.dtype).eps:
            LOGGER.warning(f'WARNING ⚠️ torch.Tensor inputs should be normalized 0.0-1.0 but max value is {im.max()}. Dividing input by 255.')
            im = im.float() / 255.0
        return im

    def __iter__(self):
        """Yields an iterator object for iterating through tensor image data."""
        self.count = 0
        return self

    def __next__(self):
        """Yields the next batch of tensor images and metadata for processing."""
        if self.count == 1:
            raise StopIteration
        self.count += 1
        return (self.paths, self.im0, [''] * self.bs)

    def __len__(self):
        """Returns the batch size of the tensor input."""
        return self.bs