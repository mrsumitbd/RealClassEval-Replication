import numpy as np
import cv2


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
            raise ValueError("new_shape must be int or (h, w)")
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
        labels = {} if labels is None else labels
        img = image if image is not None else labels.get(
            "img", labels.get("image"))
        if img is None:
            raise ValueError(
                "An image must be provided either via `image` argument or labels['img'].")

        shape = img.shape[:2]  # (h, w)
        new_h, new_w = int(self.new_shape[0]), int(self.new_shape[1])

        if self.scaleFill:
            # Stretch to fill without keeping aspect ratio
            r_w, r_h = new_w / shape[1], new_h / shape[0]
            ratio = (r_w, r_h)
            new_unpad = (new_w, new_h)  # (w, h)
            dw, dh = 0.0, 0.0
        else:
            # Keep aspect ratio
            r = min(new_h / shape[0], new_w / shape[1])
            if not self.scaleup:
                r = min(r, 1.0)
            ratio = (r, r)
            new_unpad = (int(round(shape[1] * r)),
                         int(round(shape[0] * r)))  # (w, h)
            dw = new_w - new_unpad[0]  # width padding
            dh = new_h - new_unpad[1]  # height padding
            if self.auto:
                dw %= self.stride
                dh %= self.stride
            if self.center:
                dw /= 2
                dh /= 2

        # Resize
        if (shape[1], shape[0]) != (new_unpad[0], new_unpad[1]):
            scale_factor = (new_unpad[0] / shape[1], new_unpad[1] / shape[0])
            # Choose interpolation based on scaling direction
            interp = cv2.INTER_LINEAR if max(
                scale_factor) > 1.0 else cv2.INTER_AREA
            img = cv2.resize(img, new_unpad, interpolation=interp)

        # Padding
        top, bottom = int(np.floor(dh)), int(np.ceil(dh))
        left, right = int(np.floor(dw)), int(np.ceil(dw))
        if img.ndim == 2 or (img.ndim == 3 and img.shape[2] == 1):
            color = (114,)
        else:
            color = (114, 114, 114)
        img_padded = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color)

        # Prepare outputs
        ratio_pad = (ratio, (dw, dh))
        if isinstance(labels, dict) and len(labels) > 0:
            out_labels = dict(labels)
            out_labels["img"] = img_padded
            out_labels["ratio"] = ratio
            out_labels["pad"] = (dw, dh)
            out_labels["ratio_pad"] = ratio_pad
            out_labels["new_shape"] = (
                img_padded.shape[0], img_padded.shape[1])
            out_labels["resized_shape"] = (
                img_padded.shape[0], img_padded.shape[1])

            out_labels = self._update_labels(out_labels, ratio, dw, dh)
            return out_labels
        else:
            return img_padded, ratio_pad

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

        def _to_numpy(x):
            if x is None:
                return None
            if isinstance(x, np.ndarray):
                return x
            try:
                # Try array-like conversion
                return np.asarray(x)
            except Exception:
                return None

        def _assign_attr(obj, name, value):
            try:
                setattr(obj, name, value)
            except Exception:
                try:
                    # Try in-place update if possible
                    getattr(obj, name)[...] = value
                except Exception:
                    pass

        def _clip_xyxy(arr, width, height):
            arr[:, [0, 2]] = np.clip(arr[:, [0, 2]], 0, width)
            arr[:, [1, 3]] = np.clip(arr[:, [1, 3]], 0, height)
            return arr

        inst = labels.get("instances", None)

        # Determine output canvas size for clipping if available
        img = labels.get("img", labels.get("image", None))
        out_h = img.shape[0] if isinstance(img, np.ndarray) else None
        out_w = img.shape[1] if isinstance(img, np.ndarray) else None

        # Top-level bboxes support (e.g., labels['bboxes'])
        top_bboxes = _to_numpy(labels.get("bboxes", None))
        if top_bboxes is not None and top_bboxes.ndim == 2 and top_bboxes.shape[1] == 4:
            # Assume xyxy
            b = top_bboxes.copy()
            b[:, [0, 2]] = b[:, [0, 2]] * rw + padw
            b[:, [1, 3]] = b[:, [1, 3]] * rh + padh
            if out_w is not None and out_h is not None:
                b = _clip_xyxy(b, out_w, out_h)
            labels["bboxes"] = b

        if inst is None:
            return labels

        # Boxes in xyxy
        xyxy = _to_numpy(getattr(inst, "xyxy", None))
        if xyxy is not None and xyxy.ndim == 2 and xyxy.shape[1] == 4:
            new_xyxy = xyxy.copy()
            new_xyxy[:, [0, 2]] = new_xyxy[:, [0, 2]] * rw + padw
            new_xyxy[:, [1, 3]] = new_xyxy[:, [1, 3]] * rh + padh
            if out_w is not None and out_h is not None:
                new_xyxy = _clip_xyxy(new_xyxy, out_w, out_h)
            _assign_attr(inst, "xyxy", new_xyxy)

        # Boxes alternative attributes
        for name in ("boxes", "bboxes"):
            boxes = _to_numpy(getattr(inst, name, None))
            if boxes is not None and boxes.ndim == 2 and boxes.shape[1] == 4:
                b = boxes.copy()
                # Treat as xyxy by default
                b[:, [0, 2]] = b[:, [0, 2]] * rw + padw
                b[:, [1, 3]] = b[:, [1, 3]] * rh + padh
                if out_w is not None and out_h is not None:
                    b = _clip_xyxy(b, out_w, out_h)
                _assign_attr(inst, name, b)

        # xywh (top-left origin assumption)
        xywh = _to_numpy(getattr(inst, "xywh", None))
        if xywh is not None and xywh.ndim == 2 and xywh.shape[1] == 4:
            new_xywh = xywh.copy()
            new_xywh[:, 0] = new_xywh[:, 0] * rw + padw
            new_xywh[:, 1] = new_xywh[:, 1] * rh + padh
            new_xywh[:, 2] = new_xywh[:, 2] * rw
            new_xywh[:, 3] = new_xywh[:, 3] * rh
            _assign_attr(inst, "xywh", new_xywh)

        # Segments: list of Nx2 arrays
        segments = getattr(inst, "segments", None)
        if segments is not None:
            new_segments = []
            for seg in segments:
                s = _to_numpy(seg)
                if s is None:
                    new_segments.append(seg)
                    continue
                s = s.copy()
                if s.ndim == 2 and s.shape[1] >= 2:
                    s[:, 0] = s[:, 0] * rw + padw
                    s[:, 1] = s[:, 1] * rh + padh
                    if out_w is not None and out_h is not None:
                        s[:, 0] = np.clip(s[:, 0], 0, out_w)
                        s[:, 1] = np.clip(s[:, 1], 0, out_h)
                new_segments.append(s)
            try:
                inst.segments = new_segments
            except Exception:
                pass

        # Keypoints: (N, K, 2 or 3)
        kpts = _to_numpy(getattr(inst, "keypoints", None))
        if kpts is not None and kpts.ndim == 3 and kpts.shape[-1] >= 2:
            new_kpts = kpts.copy()
            new_kpts[..., 0] = new_kpts[..., 0] * rw + padw
            new_kpts[..., 1] = new_kpts[..., 1] * rh + padh
            if out_w is not None and out_h is not None:
                new_kpts[..., 0] = np.clip(new_kpts[..., 0], 0, out_w)
                new_kpts[..., 1] = np.clip(new_kpts[..., 1], 0, out_h)
            _assign_attr(inst, "keypoints", new_kpts)

        labels["instances"] = inst
        return labels
