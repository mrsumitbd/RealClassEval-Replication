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
        # Get image
        if image is None:
            if labels is None or "img" not in labels:
                raise ValueError(
                    "Either 'image' or 'labels[\"img\"]' must be provided.")
            img = labels["img"]
        else:
            img = image

        shape = img.shape[:2]  # current shape [height, width]
        new_shape = self.new_shape

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not self.scaleup:
            r = min(r, 1.0)

        # Compute padding
        if self.scaleFill:
            ratio = (new_shape[1] / shape[1],
                     new_shape[0] / shape[0])  # width, height
            new_unpad = (new_shape[1], new_shape[0])
            dw, dh = 0, 0
        else:
            ratio = (r, r)
            new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
            dw = new_shape[1] - new_unpad[0]
            dh = new_shape[0] - new_unpad[1]

            if self.auto:
                # Make padding a multiple of stride
                dw = np.mod(dw, self.stride)
                dh = np.mod(dh, self.stride)

        if self.center:
            dw /= 2  # divide padding into 2 sides
            dh /= 2
            top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
            left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        else:
            top, bottom = 0, int(round(dh))
            left, right = 0, int(round(dw))

        # Resize image
        if self.scaleFill:
            interp = cv2.INTER_LINEAR if (
                img.shape[0] < new_shape[0] or img.shape[1] < new_shape[1]) else cv2.INTER_AREA
            img_resized = cv2.resize(
                img, (new_shape[1], new_shape[0]), interpolation=interp)
        else:
            interp = cv2.INTER_LINEAR if r > 1.0 else cv2.INTER_AREA
            img_resized = cv2.resize(
                img, (new_unpad[0], new_unpad[1]), interpolation=interp)
            img_resized = cv2.copyMakeBorder(
                img_resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))

        # Update labels if present
        if labels is not None:
            updated_labels = dict(labels)
            updated_labels["img"] = img_resized
            updated_labels["shape"] = img_resized.shape
            updated_labels["ratio_pad"] = (ratio, (left, top))
            if "instances" in labels and labels["instances"] is not None:
                updated_labels["instances"] = self._update_labels(
                    labels, ratio, left, top)
            return updated_labels
        else:
            return img_resized, (ratio, (left, top))

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
        # This assumes labels["instances"] is an object with a .boxes attribute (Nx4 array) and possibly .keypoints, .masks, etc.
        instances = labels.get("instances", None)
        if instances is None:
            return None

        # Update bounding boxes
        if hasattr(instances, "boxes"):
            boxes = instances.boxes
            # boxes: (N, 4) in xyxy format
            boxes = boxes.astype(np.float32)
            boxes[:, [0, 2]] = boxes[:, [0, 2]] * ratio[0] + padw  # x1, x2
            boxes[:, [1, 3]] = boxes[:, [1, 3]] * ratio[1] + padh  # y1, y2
            instances.boxes = boxes

        # Update keypoints if present
        if hasattr(instances, "keypoints") and instances.keypoints is not None:
            keypoints = instances.keypoints
            keypoints = keypoints.astype(np.float32)
            keypoints[..., 0] = keypoints[..., 0] * ratio[0] + padw
            keypoints[..., 1] = keypoints[..., 1] * ratio[1] + padh
            instances.keypoints = keypoints

        # Update masks if present
        if hasattr(instances, "masks") and instances.masks is not None:
            # Resize masks to new image size
            masks = instances.masks
            # masks: (N, H, W)
            new_h = int(round(labels["img"].shape[0]))
            new_w = int(round(labels["img"].shape[1]))
            new_masks = []
            for mask in masks:
                mask_resized = cv2.resize(mask.astype(
                    np.uint8), (new_w, new_h), interpolation=cv2.INTER_NEAREST)
                new_masks.append(mask_resized)
            instances.masks = np.stack(new_masks, axis=0)

        return instances
