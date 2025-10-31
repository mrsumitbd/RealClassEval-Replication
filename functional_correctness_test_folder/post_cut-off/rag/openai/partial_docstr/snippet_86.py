
import numpy as np
import cv2
from typing import Dict, Tuple, Any, Optional, List, Union


class LetterBox:
    '''
    Resize image and padding for detection, instance segmentation, pose.
    This class resizes and pads images to a specified shape while preserving aspect ratio. It also updates
    corresponding labels and bounding boxes.
    Attributes:
        new_shape (tuple): Target shape (height, width) for resizing.
        auto (bool): Whether to use minimum rectangle.
        scaleFill (bool): Whether to stretch the image to new_shape.
        scaleup (bool): Whether to allow scaling up. If False, only scale down.
        stride (int): Stride for rounding padding.
        center (bool): Whether to center the image or align to top-left.
    Methods:
        __call__: Resize and pad image, update labels and bounding boxes.
    Examples:
        >>> transform = LetterBox(new_shape=(640, 640))
        >>> result = transform(labels)
        >>> resized_img = result["img"]
        >>> updated_instances = result["instances"]
    '''

    def __init__(self, new_shape: Tuple[int, int] = (640, 640), auto: bool = False,
                 scaleFill: bool = False, scaleup: bool = True, center: bool = True,
                 stride: int = 32):
        '''
        Initialize LetterBox object for resizing and padding images.
        This class is designed to resize and pad images for object detection, instance segmentation, and pose estimation
        tasks. It supports various resizing modes including auto-sizing, scale-fill, and letterboxing.
        Args:
            new_shape (Tuple[int, int]): Target size (height, width) for the resized image.
            auto (bool): If True, use minimum rectangle to resize. If False, use new_shape directly.
            scaleFill (bool): If True, stretch the image to new_shape without padding.
            scaleup (bool): If True, allow scaling up. If False, only scale down.
            center (bool): If True, center the placed image. If False, place image in top-left corner.
            stride (int): Stride of the model (e.g., 32 for YOLOv5).
        '''
        self.new_shape = new_shape
        self.auto = auto
        self.scaleFill = scaleFill
        self.scaleup = scaleup
        self.center = center
        self.stride = stride

    def __call__(self, labels: Optional[Dict[str, Any]] = None,
                 image: Optional[np.ndarray] = None) -> Union[Dict[str, Any], Tuple[np.ndarray, Tuple[float, Tuple[int, int]]]]:
        '''
        Resizes and pads an image for object detection, instance segmentation, or pose estimation tasks.
        This method applies letterboxing to the input image, which involves resizing the image while maintaining its
        aspect ratio and adding padding to fit the new shape. It also updates any associated labels accordingly.
        Args:
            labels (Dict | None): A dictionary containing image data and associated labels, or empty dict if None.
            image (np.ndarray | None): The input image as a numpy array. If None, the image is taken from 'labels'.
        Returns:
            (Dict | Tuple): If 'labels' is provided, returns an updated dictionary with the resized and padded image,
                updated labels, and additional metadata. If 'labels' is empty, returns a tuple containing the resized
                and padded image, and a tuple of (ratio, (left_pad, top_pad)).
        '''
        if image is None:
            if labels is None or 'img' not in labels:
                raise ValueError(
                    "Either image or labels['img'] must be provided.")
            image = labels['img']

        h0, w0 = image.shape[:2]
        new_h, new_w = self.new_shape

        # Compute scaling ratio
        if self.scaleFill:
            ratio_w = new_w / w0
            ratio_h = new_h / h0
            ratio = (ratio_w, ratio_h)
            resized = cv2.resize(image, (new_w, new_h),
                                 interpolation=cv2.INTER_LINEAR)
            padw, padh = 0, 0
        else:
            if self.auto:
                # use the smaller ratio to keep aspect ratio
                ratio = min(new_h / h0, new_w / w0)
            else:
                ratio = min(new_h / h0, new_w / w0)
                if not self.scaleup:
                    ratio = min(1.0, ratio)
            ratio_w = ratio_h = ratio
            new_w = int(round(w0 * ratio))
            new_h = int(round(h0 * ratio))
            resized = cv2.resize(image, (new_w, new_h),
                                 interpolation=cv2.INTER_LINEAR)

            # Pad to target shape
            if self.center:
                # placeholder, will be overwritten
                padw = int((new_w - new_w) / 2)
                padh = int((new_h - new_h) / 2)
            else:
                padw = 0
                padh = 0

            # Compute padding to make dimensions divisible by stride
            padw = int((new_w - new_w) / 2)  # placeholder
            padh = int((new_h - new_h) / 2)  # placeholder

            # Actually compute padding
            padw = int((new_w - new_w) /
