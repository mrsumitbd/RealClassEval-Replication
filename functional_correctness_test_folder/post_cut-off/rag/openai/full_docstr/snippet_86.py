
import numpy as np
import cv2
from typing import Dict, Tuple, Any, List, Union


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

    def __init__(self, new_shape=(640, 640), auto=False, scaleFill=False, scaleup=True, center=True, stride=32):
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
        self.new_shape = tuple(new_shape)
        self.auto = auto
        self.scaleFill = scaleFill
        self.scaleup = scaleup
        self.center = center
        self.stride = stride

    def __call__(self, labels: Dict[str, Any] = None, image: np.ndarray = None):
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
        Examples:
            >>> letterbox = LetterBox(new_shape=(640, 640))
            >>> result = letterbox(labels={"img": np.zeros((480, 640, 3)), "instances": Instances(...)})
            >>> resized_img = result["img"]
            >>> updated_instances = result["instances"]
        '''
        if image is None:
            if labels is None or 'img' not in labels:
                raise ValueError(
                    "Either image or labels['img'] must be provided.")
            image = labels['img']

        h0, w0 = image.shape[:2]
        new_h, new_w = self.new_shape

        # Compute scaling ratio
        if self.auto:
            r = min(new_w / w0, new_h / h0)
        elif self.scaleFill:
            r = max(new_w / w0, new_h / h0)
        else:
            r = min(new_w / w0, new_h / h0)

        if not self.scaleup:
            r = min(r, 1.0)

        # Compute new unpadded dimensions
        new_unpad_w = int(round(w0 * r))
        new_unpad_h = int(round(h0 * r))

        # Compute padding
        dw = new_w - new_unpad_w
        dh = new_h - new_unpad_h

        # Make padding divisible by stride
        dw = int(np.mod(dw, self.stride))
        dh = int(np.mod(dh, self.stride))

        if self.center:
            dw /= 2
            dh /= 2
        else:
            dw = 0
            dh = 0

        left_pad = int(round(dw))
        top_pad = int(round(dh))
        right_pad = new_w - new_unpad_w - left_pad
        bottom_pad = new_h - new_unpad_h - top_pad

        # Resize image
        resized = cv2.resize(image, (new_unpad_w, new_unpad_h),
                             interpolation=cv2.INTER_LINEAR)

        # Pad image
        padded = cv2.copyMakeBorder(
            resized,
            top=top_pad,
            bottom=bottom_pad,
            left=left_pad,
            right=right_pad,
            borderType=cv2.BORDER_CONSTANT,
            value=(114, 114, 114)  # default padding color
        )

        # Prepare output
        if labels is not None:
            # Update labels
            updated_labels = self._update_labels(
                labels, (r, r), left_pad, top_pad)
            updated_labels['img'] = padded
            updated_labels['ratio'] = (r, r)
            updated_labels['pad'] = (left_pad, top_pad)
            updated_labels['original_shape'] = (h0, w0)
            updated_labels['new_shape'] = (new_h, new_w)
            return updated_labels
        else:
            return padded, (r, r), (left_pad, top_pad)

    @staticmethod
    def _update_labels(labels: Dict[str, Any], ratio: Tuple[float, float], padw: float, padh: float):
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
        Examples:
            >>> letterbox = LetterBox(new_shape=(640, 640))
            >>> labels = {"instances": Instances(...)}
            >>> ratio = (0.5, 0.5)
            >>> padw, padh = 10, 20
            >>> updated_labels = letterbox._update_labels(labels, ratio, padw, padh)
        '''
        if 'instances' not in labels:
            return labels

        instances = labels['instances']

        # Helper to update a single bbox
        def
