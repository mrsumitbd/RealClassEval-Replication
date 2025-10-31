
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
            img = cv2.resize(
                img, new_shape[::-1], interpolation=cv2.INTER_LINEAR)
        else:
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
            img = cv2.copyMakeBorder(
                img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))

        # Update labels if present
        if labels is not None:
            updated_labels = dict(labels)
            updated_labels["img"] = img
            if "instances" in labels and labels["instances"] is not None:
                updated_labels = self._update_labels(
                    updated_labels, ratio, left, top)
            updated_labels["shape"] = img.shape
            updated_labels["ratio_pad"] = (ratio, (left, top))
            return updated_labels
        else:
            return img, (ratio, (left, top))

    @staticmethod
    def _update_labels(labels, ratio, padw, padh):
        '''
        Updates labels after applying letterboxing to an image.
        '''
        if "instances" not in labels or labels["instances"] is None:
            return labels

        instances = labels["instances"]

        # Try to update bboxes and masks if present
        if hasattr(instances, "boxes"):
            # Assume boxes is Nx4 array: (x1, y1, x2, y2)
            boxes = instances.boxes
            boxes = boxes.astype(np.float32)
            boxes[:, [0, 2]] = boxes[:, [0, 2]] * ratio[0] + padw
            boxes[:, [1, 3]] = boxes[:, [1, 3]] * ratio[1] + padh
            instances.boxes = boxes

        if hasattr(instances, "keypoints"):
            # Assume keypoints is NxKx2 array: (x, y)
            keypoints = instances.keypoints
            keypoints = keypoints.astype(np.float32)
            keypoints[..., 0] = keypoints[..., 0] * ratio[0] + padw
            keypoints[..., 1] = keypoints[..., 1] * ratio[1] + padh
            instances.keypoints = keypoints

        if hasattr(instances, "masks"):
            # Assume masks is a list of binary masks or a numpy array
            masks = instances.masks
            if isinstance(masks, np.ndarray):
                # Resize each mask
                new_masks = []
                for mask in masks:
                    mask = cv2.resize(mask.astype(
                        np.uint8), (labels["img"].shape[1], labels["img"].shape[0]), interpolation=cv2.INTER_NEAREST)
                    new_masks.append(mask)
                instances.masks = np.stack(new_masks)
            elif isinstance(masks, list):
                new_masks = []
                for mask in masks:
                    mask = cv2.resize(mask.astype(
                        np.uint8), (labels["img"].shape[1], labels["img"].shape[0]), interpolation=cv2.INTER_NEAREST)
                    new_masks.append(mask)
                instances.masks = new_masks

        labels["instances"] = instances
        return labels
