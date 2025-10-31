import math
from typing import Tuple, Dict, Any, Optional

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
        assert isinstance(new_shape, (tuple, list)) and len(
            new_shape) == 2, "new_shape must be (h, w)"
        self.new_shape = (int(new_shape[0]), int(new_shape[1]))
        self.auto = bool(auto)
        self.scaleFill = bool(scaleFill)
        self.scaleup = bool(scaleup)
        self.center = bool(center)
        self.stride = int(stride)
        self.border_color = (114, 114, 114)

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
        if labels is None and image is None:
            raise ValueError("Either 'labels' or 'image' must be provided")

        if image is None:
            if not isinstance(labels, dict) or "img" not in labels:
                raise ValueError(
                    "labels must be a dict containing key 'img' if image is None")
            image = labels["img"]

        if image is None:
            raise ValueError("Input image is None")

        img = image
        shape = img.shape[:2]  # (h, w)
        h0, w0 = shape
        new_h, new_w = self.new_shape

        if self.scaleFill:
            r_w = new_w / w0
            r_h = new_h / h0
            ratio = (r_w, r_h)
            resize_w, resize_h = new_w, new_h
            dw = dh = 0.0
        else:
            r = min(new_h / h0, new_w / w0)
            if not self.scaleup:
                r = min(r, 1.0)
            resize_w, resize_h = int(round(w0 * r)), int(round(h0 * r))
            ratio = (resize_w / w0 if w0 else 1.0,
                     resize_h / h0 if h0 else 1.0)
            dw = new_w - resize_w
            dh = new_h - resize_h

            if self.auto:
                # Use minimum rectangle that is a multiple of stride
                dw = dw % self.stride
                dh = dh % self.stride

            if self.center:
                dw /= 2
                dh /= 2
            else:
                # top-left align
                dw, dh = float(dw), float(dh)

        # Resize
        if (img.shape[1], img.shape[0]) != (resize_w, resize_h):
            interp = cv2.INTER_LINEAR if max(
                resize_h, resize_w) >= max(h0, w0) else cv2.INTER_AREA
            img = cv2.resize(img, (resize_w, resize_h), interpolation=interp)

        # Padding
        top = int(round(dh))
        bottom = int(round(new_h - resize_h - top))
        left = int(round(dw))
        right = int(round(new_w - resize_w - left))

        if img.ndim == 2:
            border_color = 114
        else:
            border_color = self.border_color

        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=border_color)

        pad = (left, top)
        ratio_xy = (ratio[0], ratio[1])

        if labels is None:
            return img, (ratio_xy, pad)

        # Update labels dict
        out = dict(labels)  # shallow copy
        out["img"] = img
        out["ori_shape"] = (h0, w0)
        out["resized_shape"] = (img.shape[0], img.shape[1])
        out["ratio_pad"] = (ratio_xy, pad)
        out["ratio"] = ratio_xy
        out["pad"] = pad

        if "instances" in out and out["instances"] is not None:
            out["instances"] = self._update_labels(
                out, ratio_xy, left, top)["instances"]

        return out

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
        instances = labels.get("instances", None)
        if instances is None:
            return labels

        rx, ry = ratio

        def _get_attr(obj, names):
            for n in names:
                if isinstance(obj, dict) and n in obj:
                    return obj[n], n, True
                if hasattr(obj, n):
                    return getattr(obj, n), n, False
            return None, None, None

        def _set_attr(obj, name, value, is_dict):
            if name is None:
                return
            if is_dict:
                obj[name] = value
            else:
                setattr(obj, name, value)

        # Update bounding boxes in xyxy format if present
        boxes, boxes_name, boxes_is_dict = _get_attr(
            instances, ["boxes", "bboxes", "xyxy"])
        if boxes is not None:
            arr = np.asarray(boxes).copy()
            if arr.size:
                arr = arr.astype(np.float32)
                arr[:, [0, 2]] = arr[:, [0, 2]] * rx + padw
                arr[:, [1, 3]] = arr[:, [1, 3]] * ry + padh
            _set_attr(instances, boxes_name, arr, boxes_is_dict)

        # Update segments (list/array of Nx2 points per instance)
        segments, seg_name, seg_is_dict = _get_attr(
            instances, ["segments", "masks_xy", "polygons"])
        if segments is not None:
            if isinstance(segments, (list, tuple)):
                new_segments = []
                for seg in segments:
                    s = np.asarray(seg, dtype=np.float32)
                    if s.ndim == 1:
                        # flat format x1,y1,x2,y2,...
                        s[0::2] = s[0::2] * rx + padw
                        s[1::2] = s[1::2] * ry + padh
                    else:
                        s[:, 0] = s[:, 0] * rx + padw
                        s[:, 1] = s[:, 1] * ry + padh
                    new_segments.append(s)
                _set_attr(instances, seg_name, new_segments, seg_is_dict)
            else:
                s = np.asarray(segments, dtype=np.float32)
                if s.ndim == 3:
                    s[:, :, 0] = s[:, :, 0] * rx + padw
                    s[:, :, 1] = s[:, :, 1] * ry + padh
                elif s.ndim == 2:
                    s[:, 0] = s[:, 0] * rx + padw
                    s[:, 1] = s[:, 1] * ry + padh
                _set_attr(instances, seg_name, s, seg_is_dict)

        # Update keypoints (NxKx3 or NxKx2)
        kpts, kpts_name, kpts_is_dict = _get_attr(
            instances, ["keypoints", "kpts"])
        if kpts is not None:
            arr = np.asarray(kpts).copy()
            if arr.ndim >= 3 and arr.shape[-1] >= 2:
                arr[..., 0] = arr[..., 0] * rx + padw
                arr[..., 1] = arr[..., 1] * ry + padh
            _set_attr(instances, kpts_name, arr, kpts_is_dict)

        labels["instances"] = instances
        return labels
