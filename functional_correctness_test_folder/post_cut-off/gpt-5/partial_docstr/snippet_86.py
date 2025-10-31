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
            raise ValueError("new_shape must be int or (h, w) tuple")
        self.new_shape = (int(new_shape[0]), int(new_shape[1]))
        self.auto = bool(auto)
        self.scaleFill = bool(scaleFill)
        self.scaleup = bool(scaleup)
        self.center = bool(center)
        self.stride = int(stride)

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
        if labels is None:
            labels = {}
        if image is None:
            if "img" not in labels:
                raise ValueError(
                    "Image must be provided either via 'image' argument or labels['img']")
            img = labels["img"]
        else:
            img = image

        if img is None:
            raise ValueError("Input image is None")

        shape = img.shape[:2]  # (h, w)
        new_h, new_w = int(self.new_shape[0]), int(self.new_shape[1])

        if self.scaleFill:
            r_w = new_w / shape[1]
            r_h = new_h / shape[0]
            ratio = (r_w, r_h)
            new_unpad = (new_w, new_h)
            dw, dh = 0.0, 0.0
        else:
            r = min(new_h / shape[0], new_w / shape[1])
            if not self.scaleup:
                r = min(r, 1.0)
            ratio = (r, r)
            new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
            dw = new_w - new_unpad[0]
            dh = new_h - new_unpad[1]
            if self.auto and self.stride > 1:
                dw = dw % self.stride
                dh = dh % self.stride

        if self.center:
            left, right = int(np.floor(dw / 2)), int(np.ceil(dw / 2))
            top, bottom = int(np.floor(dh / 2)), int(np.ceil(dh / 2))
        else:
            left, right = 0, int(round(dw))
            top, bottom = 0, int(round(dh))

        if shape[::-1] != tuple(new_unpad):
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)

        color = (114, 114, 114)
        if img.ndim == 2:
            # grayscale
            img = cv2.copyMakeBorder(
                img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color[0])
        else:
            img = cv2.copyMakeBorder(
                img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

        padw, padh = float(left), float(top)

        if labels:
            labels = dict(labels)  # shallow copy
            labels["img"] = img
            labels["ori_shape"] = labels.get("ori_shape", tuple(shape))
            labels["new_shape"] = img.shape[:2]
            labels["ratio"] = ratio
            labels["pad"] = (padw, padh)
            labels["ratio_pad"] = (ratio, (padw, padh))
            labels = self._update_labels(labels, ratio, padw, padh)
            return labels
        else:
            return img, (ratio, (padw, padh))

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
        rw, rh = float(ratio[0]), float(ratio[1])

        def _scale_pad_boxes(boxes):
            # boxes expected as Nx4 in xyxy
            if boxes is None:
                return boxes
            b = np.asarray(boxes, dtype=np.float32)
            if b.ndim == 1 and b.size == 4:
                b = b[None, :]
            if b.shape[-1] != 4:
                return boxes
            b[:, [0, 2]] = b[:, [0, 2]] * rw + padw
            b[:, [1, 3]] = b[:, [1, 3]] * rh + padh
            return b

        def _scale_pad_segments(segments):
            if segments is None:
                return segments
            new_segments = []
            for seg in segments:
                arr = np.asarray(seg, dtype=np.float32)
                if arr.ndim != 2 or arr.shape[1] < 2:
                    new_segments.append(seg)
                    continue
                arr[:, 0] = arr[:, 0] * rw + padw
                arr[:, 1] = arr[:, 1] * rh + padh
                new_segments.append(arr)
            return new_segments

        def _scale_pad_keypoints(kpts):
            if kpts is None:
                return kpts
            arr = np.asarray(kpts, dtype=np.float32)
            if arr.ndim < 2:
                return kpts
            # shapes: (N, K, 2|3) or (K, 2|3)
            if arr.ndim == 2:
                # (K, C)
                if arr.shape[-1] >= 2:
                    arr[..., 0] = arr[..., 0] * rw + padw
                    arr[..., 1] = arr[..., 1] * rh + padh
                return arr
            else:
                # (N, K, C)
                if arr.shape[-1] >= 2:
                    arr[..., 0] = arr[..., 0] * rw + padw
                    arr[..., 1] = arr[..., 1] * rh + padh
                return arr

        # Update common label formats in labels dict
        # 1) Top-level arrays
        for key in ("bboxes", "boxes", "xyxy"):
            if key in labels:
                scaled = _scale_pad_boxes(labels[key])
                if scaled is not None:
                    labels[key] = scaled

        if "segments" in labels:
            labels["segments"] = _scale_pad_segments(labels["segments"])

        for key in ("keypoints", "kpts"):
            if key in labels:
                scaled_kpts = _scale_pad_keypoints(labels[key])
                if scaled_kpts is not None:
                    labels[key] = scaled_kpts

        # 2) Instances object or dict
        if "instances" in labels:
            inst = labels["instances"]

            # If dict-like
            if isinstance(inst, dict):
                if "bboxes" in inst:
                    inst["bboxes"] = _scale_pad_boxes(inst.get("bboxes"))
                if "boxes" in inst:
                    inst["boxes"] = _scale_pad_boxes(inst.get("boxes"))
                if "xyxy" in inst:
                    inst["xyxy"] = _scale_pad_boxes(inst.get("xyxy"))
                if "segments" in inst:
                    inst["segments"] = _scale_pad_segments(
                        inst.get("segments"))
                if "keypoints" in inst:
                    inst["keypoints"] = _scale_pad_keypoints(
                        inst.get("keypoints"))
                if "kpts" in inst:
                    inst["kpts"] = _scale_pad_keypoints(inst.get("kpts"))
                labels["instances"] = inst
            else:
                # Object-like with attributes
                # boxes
                for attr in ("bboxes", "boxes", "xyxy"):
                    if hasattr(inst, attr):
                        try:
                            val = getattr(inst, attr)
                            new_val = _scale_pad_boxes(val)
                            if new_val is not None:
                                setattr(inst, attr, new_val)
                        except Exception:
                            pass
                # segments
                if hasattr(inst, "segments"):
                    try:
                        setattr(inst, "segments", _scale_pad_segments(
                            getattr(inst, "segments")))
                    except Exception:
                        pass
                # keypoints
                for attr in ("keypoints", "kpts"):
                    if hasattr(inst, attr):
                        try:
                            setattr(inst, attr, _scale_pad_keypoints(
                                getattr(inst, attr)))
                        except Exception:
                            pass
                labels["instances"] = inst

        return labels
