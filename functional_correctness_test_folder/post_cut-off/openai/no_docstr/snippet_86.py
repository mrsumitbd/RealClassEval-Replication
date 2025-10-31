
import cv2
import numpy as np
from typing import Tuple, Dict, Any, List, Union


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

    def __call__(self, labels: Union[Dict[str, Any], None] = None,
                 image: Union[np.ndarray, None] = None) -> Union[Dict[str, Any], Tuple[np.ndarray, Tuple[float, float], Tuple[float, float]]]:
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
        # Get image
        if image is None:
            if labels is None or 'img' not in labels:
                raise ValueError(
                    "Either image or labels['img'] must be provided.")
            image = labels['img']
        else:
            if labels is None:
                labels = {}

        h0, w0 = image.shape[:2]
        new_h, new_w = self.new_shape

        # Compute scaling ratio
        r_w = new_w / w0
        r_h = new_h / h0
        if self.scaleFill:
            r = r_w, r_h
        else:
            r = min(r_w, r_h) if self.scaleup else min(r_w, r_h, 1.0)
            r_w = r_h = r

        # Compute new dimensions
        new_unpad_w = int(round(w0 * r_w))
        new_unpad_h = int(round(h0 * r_h))

        # Compute padding
        padw = new_w - new_unpad_w
        padh = new_h - new_unpad_h

        if self.auto:
            # Make sure padding is divisible by stride
            padw = padw % self.stride
            padh = padh % self.stride

        if self.center:
            padw_left = padw // 2
            padw_right = padw - padw_left
            padh_top = padh // 2
            padh_bottom = padh - padh_top
        else:
            padw_left = 0
            padw_right = padw
            padh_top = 0
            padh_bottom = padh

        # Resize image
        resized = cv2.resize(image, (new_unpad_w, new_unpad_h),
                             interpolation=cv2.INTER_LINEAR)

        # Pad image
        padded = cv2.copyMakeBorder(resized, padh_top, padh_bottom, padw_left, padw_right,
                                    borderType=cv2.BORDER_CONSTANT, value=(114, 114, 114))

        # Update labels if provided
        if labels:
            updated_labels = self._update_labels(
                labels, (r_w, r_h), padw_left, padh_top)
            updated_labels['img'] = padded
            updated_labels['ratio'] = (r_w, r_h)
            updated_labels['pad'] = (padw_left, padh_top)
            updated_labels['new_shape'] = (new_h, new_w)
            return updated_labels
        else:
            return padded, (r_w, r_h), (padw_left, padh_top)

    @staticmethod
    def _update_labels(labels: Dict[str, Any], ratio: Tuple[float, float],
                       padw: float, padh: float) -> Dict[str, Any]:
        '''
        Updates labels after applying letterboxing to an image.
        This method modifies the bounding box coordinates of instances in the labels
        to account for resizing and padding applied during letterboxing.
        Args:
            labels (Dict): A dictionary containing image labels and instances.
            ratio (Tuple[float, float]): Scaling ratios (width, height) applied to the image.
            padw (float): Padding width added to the image.
            padh (float): Padding height added to the image.
        Returns:
            (Dict): Updated labels dictionary with modified instance coordinates.
        '''
        if 'instances' not in labels:
            return labels

        instances = labels['instances']
        if isinstance(instances, list):
            # Assume each instance is a dict with 'bbox' key
            for inst in instances:
                if 'bbox' in inst:
                    x1, y1, x2, y2 = inst['bbox']
                    x1 = x1 * ratio[0] + padw
                    y1 = y1 * ratio[1] + padh
                    x2 = x2 * ratio[0] + padw
                    y2 = y2 * ratio[1] + padh
                    inst['bbox'] = [x1, y1, x2, y2]
                elif 'boxes' in inst and isinstance(inst['boxes'], np.ndarray):
                    # boxes shape (N,4)
                    inst['boxes'] = inst['boxes'] * \
                        np.array([ratio[0], ratio[1], ratio[0], ratio[1]])
                    inst['boxes'][:, [0
