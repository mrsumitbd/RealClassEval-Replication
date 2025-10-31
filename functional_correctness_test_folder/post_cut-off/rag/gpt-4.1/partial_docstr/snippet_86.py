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
        self.new_shape = new_shape
        self.auto = auto
        self.scaleFill = scaleFill
        self.scaleup = scaleup
        self.center = center
        self.stride = stride

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
        # Get image
        if image is None:
            if labels is None or "img" not in labels:
                raise ValueError("No image provided.")
            img = labels["img"]
        else:
            img = image

        shape = img.shape[:2]  # current shape [height, width]
        new_shape = self.new_shape

        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)
        h0, w0 = shape
        h1, w1 = new_shape

        # Scale ratio (new / old)
        r = min(h1 / h0, w1 / w0)
        if not self.scaleup:
            r = min(r, 1.0)

        # Compute padding
        if self.scaleFill:
            r = h1 / h0, w1 / w0  # stretch
            ratio = (r[1], r[0])
            new_unpad = (int(round(w0 * r[1])), int(round(h0 * r[0])))
            dw, dh = 0, 0
        else:
            ratio = (r, r)
            new_unpad = (int(round(w0 * r)), int(round(h0 * r)))
            dw, dh = w1 - new_unpad[0], h1 - new_unpad[1]

            if self.auto:
                # minimum rectangle
                dw, dh = np.mod(dw, self.stride), np.mod(dh, self.stride)

        if self.center:
            dw /= 2  # divide padding into 2 sides
            dh /= 2
        else:
            dw, dh = 0.0, 0.0

        # Resize
        if self.scaleFill:
            interp = cv2.INTER_LINEAR
            img = cv2.resize(img, (w1, h1), interpolation=interp)
            padw, padh = 0, 0
        else:
            interp = cv2.INTER_LINEAR
            img = cv2.resize(img, new_unpad, interpolation=interp)
            top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
            left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
            padw, padh = left, top
            img = cv2.copyMakeBorder(
                img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))

        # Update labels if present
        if labels is not None:
            updated_labels = self._update_labels(labels, ratio, padw, padh)
            out = dict(labels)
            out["img"] = img
            out["ratio_pad"] = (ratio, (padw, padh))
            out.update(updated_labels)
            return out
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
        out = {}
        if "instances" in labels and hasattr(labels["instances"], "boxes"):
            instances = labels["instances"]
            boxes = instances.boxes
            # boxes: (N, 4) in xyxy format
            if hasattr(boxes, "clone"):
                boxes = boxes.clone()
            else:
                boxes = np.copy(boxes)
            # Scale
            boxes[:, [0, 2]] = boxes[:, [0, 2]] * ratio[0] + padw
            boxes[:, [1, 3]] = boxes[:, [1, 3]] * ratio[1] + padh
            if hasattr(instances, "boxes"):
                instances.boxes = boxes
            out["instances"] = instances
        elif "bboxes" in labels:
            # For dict with "bboxes" key (e.g. list of [x1, y1, x2, y2])
            bboxes = np.array(labels["bboxes"])
            bboxes[:, [0, 2]] = bboxes[:, [0, 2]] * ratio[0] + padw
            bboxes[:, [1, 3]] = bboxes[:, [1, 3]] * ratio[1] + padh
            out["bboxes"] = bboxes
        return out
