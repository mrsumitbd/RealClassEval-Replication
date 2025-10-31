import math
from typing import Tuple, Dict, Any, Optional, Union

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
                "new_shape must be int or tuple/list of (height, width)")
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
        lbls = labels if labels is not None else {}
        img = image if image is not None else lbls.get("img", None)
        if img is None:
            raise ValueError(
                "No image provided. Pass image=... or labels['img'].")

        shape = img.shape[:2]  # (h, w)
        new_h, new_w = int(self.new_shape[0]), int(self.new_shape[1])

        if self.scaleFill:
            r_w = new_w / shape[1]
            r_h = new_h / shape[0]
            ratio = (r_w, r_h)
            new_unpad_w, new_unpad_h = new_w, new_h
            dw, dh = 0.0, 0.0
        else:
            r = min(new_h / shape[0], new_w / shape[1])
            if not self.scaleup:
                r = min(r, 1.0)
            ratio = (r, r)
            new_unpad_w, new_unpad_h = int(
                round(shape[1] * r)), int(round(shape[0] * r))
            dw = new_w - new_unpad_w
            dh = new_h - new_unpad_h
            if self.auto:
                dw = dw % self.stride
                dh = dh % self.stride

        if self.center:
            dw /= 2
            dh /= 2
            left = int(round(dw - 0.1))
            right = int(round(new_w - new_unpad_w - left))
            top = int(round(dh - 0.1))
            bottom = int(round(new_h - new_unpad_h - top))
        else:
            left, top = 0, 0
            right = int(new_w - new_unpad_w)
            bottom = int(new_h - new_unpad_h)

        if (shape[1], shape[0]) != (new_unpad_w, new_unpad_h):
            interp = cv2.INTER_LINEAR
            img = cv2.resize(img, (new_unpad_w, new_unpad_h),
                             interpolation=interp)

        pad_color = (114, 114, 114) if img.ndim == 3 else 114
        img_out = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=pad_color)

        if labels is None or len(lbls) == 0:
            return img_out, (ratio, (left, top))

        lbls = dict(lbls)
        lbls["img"] = img_out
        lbls["ratio_pad"] = (ratio, (left, top))
        lbls["ori_shape"] = shape
        lbls["new_shape"] = img_out.shape[:2]
        return self._update_labels(lbls, ratio, left, top)

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
        rw, rh = ratio

        def _update_boxes_xyxy(arr: np.ndarray):
            if arr is None or arr.size == 0:
                return arr
            arr = np.asarray(arr)
            if arr.ndim == 1 and arr.shape[0] == 4:
                arr = arr[None, :]
            if arr.shape[-1] != 4:
                return arr
            arr = arr.copy()
            arr[:, [0, 2]] = arr[:, [0, 2]] * rw + padw
            arr[:, [1, 3]] = arr[:, [1, 3]] * rh + padh
            return arr

        def _update_boxes_xywh(arr: np.ndarray):
            if arr is None or arr.size == 0:
                return arr
            arr = np.asarray(arr)
            if arr.ndim == 1 and arr.shape[0] == 4:
                arr = arr[None, :]
            if arr.shape[-1] != 4:
                return arr
            arr = arr.copy()
            arr[:, 0] = arr[:, 0] * rw + padw
            arr[:, 1] = arr[:, 1] * rh + padh
            arr[:, 2] = arr[:, 2] * rw
            arr[:, 3] = arr[:, 3] * rh
            return arr

        def _update_points(arr: np.ndarray):
            if arr is None or arr.size == 0:
                return arr
            arr = np.asarray(arr)
            arr = arr.copy()
            if arr.ndim == 2 and arr.shape[1] == 2:
                arr[:, 0] = arr[:, 0] * rw + padw
                arr[:, 1] = arr[:, 1] * rh + padh
            elif arr.ndim == 3 and arr.shape[-1] >= 2:
                arr[..., 0] = arr[..., 0] * rw + padw
                arr[..., 1] = arr[..., 1] * rh + padh
            return arr

        # Update common dict-based fields
        bbox_format = labels.get("bbox_format", "xyxy")
        if "bboxes" in labels and isinstance(labels["bboxes"], np.ndarray):
            if bbox_format == "xywh":
                labels["bboxes"] = _update_boxes_xywh(labels["bboxes"])
            else:
                labels["bboxes"] = _update_boxes_xyxy(labels["bboxes"])
        if "boxes" in labels and isinstance(labels["boxes"], np.ndarray):
            # If format hint provided for boxes
            fmt = labels.get("boxes_format", bbox_format)
            if fmt == "xywh":
                labels["boxes"] = _update_boxes_xywh(labels["boxes"])
            else:
                labels["boxes"] = _update_boxes_xyxy(labels["boxes"])

        # Segments: list of (N, 2) arrays
        if "segments" in labels and labels["segments"] is not None:
            segs = labels["segments"]
            if isinstance(segs, (list, tuple)):
                updated = []
                for seg in segs:
                    if seg is None:
                        updated.append(seg)
                    else:
                        updated.append(_update_points(np.asarray(seg)))
                labels["segments"] = updated

        # Keypoints: (N, K, 2 or 3)
        if "keypoints" in labels and isinstance(labels["keypoints"], np.ndarray):
            labels["keypoints"] = _update_points(labels["keypoints"])

        # Try to update nested 'instances' if it holds numpy arrays with common names
        inst = labels.get("instances", None)
        if inst is not None:
            # dict-like
            if isinstance(inst, dict):
                if "bboxes" in inst and isinstance(inst["bboxes"], np.ndarray):
                    fmt = inst.get("bbox_format", bbox_format)
                    inst["bboxes"] = _update_boxes_xywh(
                        inst["bboxes"]) if fmt == "xywh" else _update_boxes_xyxy(inst["bboxes"])
                if "boxes" in inst and isinstance(inst["boxes"], np.ndarray):
                    fmt = inst.get("boxes_format", bbox_format)
                    inst["boxes"] = _update_boxes_xywh(
                        inst["boxes"]) if fmt == "xywh" else _update_boxes_xyxy(inst["boxes"])
                if "xyxy" in inst and isinstance(inst["xyxy"], np.ndarray):
                    inst["xyxy"] = _update_boxes_xyxy(inst["xyxy"])
                if "xywh" in inst and isinstance(inst["xywh"], np.ndarray):
                    inst["xywh"] = _update_boxes_xywh(inst["xywh"])
                if "segments" in inst and inst["segments"] is not None:
                    segs = inst["segments"]
                    if isinstance(segs, (list, tuple)):
                        inst["segments"] = [_update_points(np.asarray(
                            s)) if s is not None else s for s in segs]
                if "keypoints" in inst and isinstance(inst["keypoints"], np.ndarray):
                    inst["keypoints"] = _update_points(inst["keypoints"])
                labels["instances"] = inst
            else:
                # object-like with numpy array attributes
                for attr_name in ("xyxy", "xywh", "bboxes", "boxes"):
                    if hasattr(inst, attr_name):
                        arr = getattr(inst, attr_name)
                        if isinstance(arr, np.ndarray):
                            if attr_name in ("xywh",):
                                setattr(inst, attr_name,
                                        _update_boxes_xywh(arr))
                            else:
                                setattr(inst, attr_name,
                                        _update_boxes_xyxy(arr))
                if hasattr(inst, "segments"):
                    segs = getattr(inst, "segments")
                    if isinstance(segs, (list, tuple)):
                        updated = [_update_points(np.asarray(
                            s)) if s is not None else s for s in segs]
                        try:
                            setattr(inst, "segments", updated)
                        except Exception:
                            pass
                if hasattr(inst, "keypoints"):
                    kps = getattr(inst, "keypoints")
                    if isinstance(kps, np.ndarray):
                        try:
                            setattr(inst, "keypoints", _update_points(kps))
                        except Exception:
                            pass
                labels["instances"] = inst

        return labels
