
import numpy as np
from typing import Dict, Tuple, Optional, Union


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
        Attributes:
            new_shape (Tuple[int, int]): Target size for the resized image.
            auto (bool): Flag for using minimum rectangle resizing.
            scaleFill (bool): Flag for stretching image without padding.
            scaleup (bool): Flag for allowing upscaling.
            stride (int): Stride value for ensuring image size is divisible by stride.
        Examples:
            >>> letterbox = LetterBox(new_shape=(640, 640), auto=False, scaleFill=False, scaleup=True, stride=32)
            >>> resized_img = letterbox(original_img)
        '''
        self.new_shape = new_shape
        self.auto = auto
        self.scaleFill = scaleFill
        self.scaleup = scaleup
        self.stride = stride
        self.center = center

    def __call__(self, labels=None, image=None):
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
        if image is None and labels is not None:
            image = labels.get('img') if isinstance(labels, dict) else None

        shape = image.shape[:2]  # current shape [height, width]
        new_shape = self.new_shape

        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        if self.auto:
            new_shape = (np.ceil(shape[0] / self.stride) * self.stride,
                         np.ceil(shape[1] / self.stride) * self.stride)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        # only scale down, do not scale up (for better val mAP)
        if not self.scaleup:
            r = min(r, 1.0)

        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - \
            new_unpad[1]  # wh padding

        if self.scaleFill:  # stretch
            dw, dh = 0.0, 0.0
            new_unpad = new_shape[1], new_shape[0]
            ratio = new_shape[1] / shape[1], new_shape[0] / \
                shape[0]  # width, height ratios

        if self.center:
            dw /= 2  # divide padding into 2 sides
            dh /= 2

        if shape[::-1] != new_unpad:  # resize
            image = cv2.resize(
                image, new_unpad, interpolation=cv2.INTER_LINEAR)

        top, bottom = int(round(
            dh - 0.1)) if self.center else 0, int(round(dh + 0.1)) if self.center else dh
        left, right = int(round(
            dw - 0.1)) if self.center else 0, int(round(dw + 0.1)) if self.center else dw

        image = cv2.copyMakeBorder(image, top, bottom, left, right,
                                   cv2.BORDER_CONSTANT, value=(114, 114, 114))  # add border

        if labels is None:
            return image, (ratio, (left, top))

        if isinstance(labels, dict):
            labels['img'] = image
            labels['resized_shape'] = new_shape
            if 'instances' in labels:
                labels['instances'] = self._update_labels(
                    labels['instances'], ratio, left, top)
            return labels
        else:
            return image, (ratio, (left, top))

    @staticmethod
    def _update_labels(labels, ratio, padw, padh):
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
        if hasattr(labels, 'bbox'):
            bbox = labels.bbox
            bbox[:, [0, 2]] = bbox[:, [0, 2]] * ratio[0] + padw  # xmin, xmax
            bbox[:, [1, 3]] = bbox[:, [1, 3]] * ratio[1] + padh  # ymin, ymax
            labels.bbox = bbox
        if hasattr(labels, 'keypoints'):
            keypoints = labels.keypoints
            keypoints[..., 0] = keypoints[..., 0] * ratio[0] + padw  # x
            keypoints[..., 1] = keypoints[..., 1] * ratio[1] + padh  # y
            labels.keypoints = keypoints
        return labels
