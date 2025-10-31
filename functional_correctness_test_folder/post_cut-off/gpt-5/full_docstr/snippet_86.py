import copy
from typing import Dict, Tuple, Optional, Any

import cv2
import numpy as np


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
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)
        if not (isinstance(new_shape, (tuple, list)) and len(new_shape) == 2):
            raise ValueError(
                "new_shape must be an int or a tuple/list of (height, width)")
        self.new_shape = (int(new_shape[0]), int(new_shape[1]))
        self.auto = bool(auto)
        self.scaleFill = bool(scaleFill)
        self.scaleup = bool(scaleup)
        self.center = bool(center)
        self.stride = int(stride)

    def __call__(self, labels: Optional[Dict[str, Any]] = None, image: Optional[np.ndarray] = None):
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
        if labels is None:
            labels = {}
        if image is None:
            image = labels.get("img", None)
        if image is None:
            raise ValueError(
                "No image provided. Pass image via 'image' argument or inside labels['img'].")

        img = image
        h0, w0 = img.shape[:2]
        newh, neww = self.new_shape

        if self.scaleFill:
            ratio = (neww / w0, newh / h0)
            new_unpad = (neww, newh)
            dw = dh = 0.0
        else:
            r = min(newh / h0, neww / w0)
            if not self.scaleup:
                r = min(r, 1.0)
            new_unpad = (int(round(w0 * r)), int(round(h0 * r)))
            dw = neww - new_unpad[0]
            dh = newh - new_unpad[1]
            if self.auto:
                dw %= self.stride
                dh %= self.stride
            ratio = (new_unpad[0] / w0 if w0 else 1.0,
                     new_unpad[1] / h0 if h0 else 1.0)

        if self.center:
            dw_left = dw / 2
            dh_top = dh / 2
        else:
            dw_left = 0.0
            dh_top = 0.0

        if new_unpad != (w0, h0):
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)

        top = int(round(dh_top - 0.1))
        bottom = int(round((dh - dh_top) - 0.1))
        left = int(round(dw_left - 0.1))
        right = int(round((dw - dw_left) - 0.1))

        pad_color = None
        if isinstance(labels, dict):
            pad_color = labels.get("pad_color", None)
        if pad_color is None:
            pad_color = (114, 114, 114)

        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=pad_color)

        if labels:
            out = labels.copy()
            out["img"] = img
            out["ratio_pad"] = (ratio, (dw_left, dh_top))
            out["ratio"] = ratio
            out["pad"] = (dw_left, dh_top)
            out["resized_shape"] = img.shape[:2]
            out["letterbox_params"] = {
                "new_shape": self.new_shape,
                "auto": self.auto,
                "scaleFill": self.scaleFill,
                "scaleup": self.scaleup,
                "center": self.center,
                "stride": self.stride,
                "pad_color": pad_color,
            }
            out = self._update_labels(out, ratio, dw_left, dh_top)
            return out
        else:
            return img, (ratio, (dw_left, dh_top))

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
        inst = labels.get("instances", None)
        if inst is None:
            return labels

        rx, ry = ratio

        def _set_or_assign(obj, attr, new_value):
            try:
                current = getattr(obj, attr)
                if isinstance(current, np.ndarray):
                    if current.shape == np.asarray(new_value).shape:
                        current[...] = new_value
                        return
                setattr(obj, attr, new_value)
            except Exception:
                try:
                    setattr(obj, attr, new_value)
                except Exception:
                    pass

        # Update boxes in xyxy format if available
        for attr in ("xyxy", "boxes", "bboxes"):
            if hasattr(inst, attr):
                arr = getattr(inst, attr)
                try:
                    a = np.asarray(arr).copy()
                    if a.ndim == 2 and a.shape[1] >= 4:
                        a[:, [0, 2]] = a[:, [0, 2]] * rx + padw
                        a[:, [1, 3]] = a[:, [1, 3]] * ry + padh
                        _set_or_assign(inst, attr, a)
                except Exception:
                    pass

        # Update segments (list of Nx2 arrays)
        if hasattr(inst, "segments"):
            segs = getattr(inst, "segments")
            try:
                new_segs = []
                for seg in segs:
                    s = np.asarray(seg).copy()
                    if s.ndim == 2 and s.shape[1] >= 2:
                        s[:, 0] = s[:, 0] * rx + padw
                        s[:, 1] = s[:, 1] * ry + padh
                    new_segs.append(s)
                _set_or_assign(inst, "segments", new_segs)
            except Exception:
                pass

        # Update keypoints (N,K,2 or N,K,3) last dim x,y,(v/score)
        for kp_attr in ("keypoints", "kpts", "landmarks"):
            if hasattr(inst, kp_attr):
                kps = getattr(inst, kp_attr)
                try:
                    k = np.asarray(kps).copy()
                    if k.ndim >= 3 and k.shape[-1] >= 2:
                        k[..., 0] = k[..., 0] * rx + padw
                        k[..., 1] = k[..., 1] * ry + padh
                        _set_or_assign(inst, kp_attr, k)
                except Exception:
                    pass

        # Update any stored image shape metadata if present
        for shape_attr in ("image_shape", "img_shape", "shape", "hw"):
            if hasattr(inst, shape_attr):
                try:
                    setattr(inst, shape_attr, labels.get(
                        "resized_shape", None) or getattr(inst, shape_attr))
                except Exception:
                    pass

        return labels
