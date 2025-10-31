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
        assert isinstance(new_shape, (tuple, list)) and len(
            new_shape) == 2, "new_shape must be (h, w)"
        self.new_shape = (int(new_shape[0]), int(new_shape[1]))
        self.auto = bool(auto)
        self.scaleFill = bool(scaleFill)
        self.scaleup = bool(scaleup)
        self.center = bool(center)
        self.stride = int(stride)
        self.pad_color = (114, 114, 114)

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
        img = image if image is not None else labels.get("img", None)
        if img is None:
            raise ValueError("No image provided. Pass image or labels['img'].")

        shape = img.shape[:2]  # h, w
        new_h, new_w = self.new_shape

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
            dw, dh = new_w - new_unpad[0], new_h - new_unpad[1]
            if self.auto:
                dw %= self.stride
                dh %= self.stride

        if self.center:
            left = int(np.floor(dw / 2))
            right = int(new_w - new_unpad[0] - left)
            top = int(np.floor(dh / 2))
            bottom = int(new_h - new_unpad[1] - top)
            padw, padh = float(left), float(top)
        else:
            left, top = 0, 0
            right = int(new_w - new_unpad[0])
            bottom = int(new_h - new_unpad[1])
            padw, padh = 0.0, 0.0

        if (shape[1], shape[0]) != new_unpad:
            interp = cv2.INTER_LINEAR if ratio[0] >= 1.0 or ratio[1] >= 1.0 else cv2.INTER_AREA
            img = cv2.resize(
                img, (new_unpad[0], new_unpad[1]), interpolation=interp)

        if img.ndim == 2:
            canvas = np.full(
                (new_h, new_w), self.pad_color[0], dtype=img.dtype)
        else:
            c = img.shape[2] if img.ndim == 3 else 1
            canvas = np.full((new_h, new_w, c),
                             self.pad_color, dtype=img.dtype)

        y1, y2 = top, top + new_unpad[1]
        x1, x2 = left, left + new_unpad[0]
        canvas[y1:y2, x1:x2] = img
        out_img = canvas

        if labels:
            out = dict(labels)  # shallow copy
            out["img"] = out_img
            out["ratio_pad"] = (ratio, (padw, padh))
            out["resized_shape"] = (new_h, new_w)
            out["ori_shape"] = labels.get("ori_shape", shape)
            out = self._update_labels(out, ratio, padw, padh)
            return out
        else:
            return out_img, (ratio, (padw, padh))

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
        rw, rh = ratio
        img = labels.get("img", None)
        if img is not None:
            h, w = img.shape[:2]
        else:
            w = h = None

        def _clip_xyxy(b):
            if w is None or h is None or b.size == 0:
                return b
            b[:, [0, 2]] = np.clip(b[:, [0, 2]], 0, w)
            b[:, [1, 3]] = np.clip(b[:, [1, 3]], 0, h)
            return b

        def _scale_xyxy(b):
            if b is None:
                return b
            b = np.asarray(b, dtype=np.float32)
            if b.size == 0:
                return b
            b[:, [0, 2]] = b[:, [0, 2]] * rw + padw
            b[:, [1, 3]] = b[:, [1, 3]] * rh + padh
            return _clip_xyxy(b)

        def _scale_xywh_centers(b):
            if b is None:
                return b
            b = np.asarray(b, dtype=np.float32)
            if b.size == 0:
                return b
            b[:, 0] = b[:, 0] * rw + padw
            b[:, 1] = b[:, 1] * rh + padh
            b[:, 2] = b[:, 2] * rw
            b[:, 3] = b[:, 3] * rh
            if w is not None and h is not None:
                x1 = b[:, 0] - b[:, 2] / 2
                y1 = b[:, 1] - b[:, 3] / 2
                x2 = b[:, 0] + b[:, 2] / 2
                y2 = b[:, 1] + b[:, 3] / 2
                x1 = np.clip(x1, 0, w)
                y1 = np.clip(y1, 0, h)
                x2 = np.clip(x2, 0, w)
                y2 = np.clip(y2, 0, h)
                b[:, 0] = (x1 + x2) / 2
                b[:, 1] = (y1 + y2) / 2
                b[:, 2] = np.clip(b[:, 2], 0, w)
                b[:, 3] = np.clip(b[:, 3], 0, h)
            return b

        def _scale_segments(segments):
            if segments is None:
                return segments
            out = []
            for seg in segments:
                arr = np.asarray(seg, dtype=np.float32).copy()
                if arr.ndim == 1:
                    arr = arr.reshape(-1, 2)
                if arr.size == 0:
                    out.append(arr)
                    continue
                arr[:, 0] = arr[:, 0] * rw + padw
                arr[:, 1] = arr[:, 1] * rh + padh
                if w is not None and h is not None:
                    arr[:, 0] = np.clip(arr[:, 0], 0, w)
                    arr[:, 1] = np.clip(arr[:, 1], 0, h)
                out.append(arr)
            return out

        def _scale_keypoints(kpts):
            if kpts is None:
                return kpts
            arr = np.asarray(kpts, dtype=np.float32).copy()
            if arr.size == 0:
                return arr
            if arr.ndim >= 2 and arr.shape[-1] >= 2:
                arr[..., 0] = arr[..., 0] * rw + padw
                arr[..., 1] = arr[..., 1] * rh + padh
                if w is not None and h is not None:
                    arr[..., 0] = np.clip(arr[..., 0], 0, w)
                    arr[..., 1] = np.clip(arr[..., 1], 0, h)
            return arr

        if "bboxes" in labels:
            fmt = labels.get("bbox_format", "xyxy").lower()
            if fmt == "xywh":
                labels["bboxes"] = _scale_xywh_centers(labels["bboxes"])
            else:
                labels["bboxes"] = _scale_xyxy(labels["bboxes"])

        if "segments" in labels:
            labels["segments"] = _scale_segments(labels["segments"])

        if "keypoints" in labels:
            labels["keypoints"] = _scale_keypoints(labels["keypoints"])

        inst = labels.get("instances", None)
        if inst is not None:
            if hasattr(inst, "boxes"):
                boxes = getattr(inst, "boxes")
                updated = None
                if isinstance(boxes, np.ndarray) or (hasattr(boxes, "__array__")):
                    updated = _scale_xyxy(np.asarray(boxes))
                    try:
                        setattr(inst, "boxes", updated)
                    except Exception:
                        pass
                elif isinstance(boxes, list):
                    updated = _scale_xyxy(np.array(boxes))
                    try:
                        setattr(inst, "boxes", updated)
                    except Exception:
                        pass
                elif hasattr(boxes, "xyxy"):
                    try:
                        bx = np.asarray(getattr(boxes, "xyxy"))
                        updated = _scale_xyxy(bx)
                        try:
                            setattr(boxes, "xyxy", updated)
                        except Exception:
                            pass
                    except Exception:
                        pass

            if hasattr(inst, "segments"):
                segs = getattr(inst, "segments")
                try:
                    updated_segs = _scale_segments(segs)
                    setattr(inst, "segments", updated_segs)
                except Exception:
                    pass

            if hasattr(inst, "keypoints"):
                kpts = getattr(inst, "keypoints")
                try:
                    updated_kpts = _scale_keypoints(kpts)
                    setattr(inst, "keypoints", updated_kpts)
                except Exception:
                    pass

        return labels
