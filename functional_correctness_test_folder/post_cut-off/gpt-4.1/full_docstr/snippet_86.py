
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
        if labels is not None:
            img = labels.get("img", None) if image is None else image
        else:
            img = image
        if img is None:
            raise ValueError("No image provided.")

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
                # make padding a multiple of stride
                dw = np.mod(dw, self.stride)
                dh = np.mod(dh, self.stride)
            if self.center:
                dw /= 2  # divide padding into 2 sides
                dh /= 2
            else:
                dw = 0
                dh = 0

        # Resize
        if (shape[1], shape[0]) != new_unpad:
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)

        # Padding
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))

        if labels is not None:
            updated_labels = self._update_labels(labels, ratio, left, top)
            updated_labels["img"] = img
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
        import copy
        labels = copy.deepcopy(labels)
        if "instances" in labels and hasattr(labels["instances"], "boxes"):
            boxes = labels["instances"].boxes
            # boxes: (N, 4) in xyxy format
            if isinstance(boxes, np.ndarray):
                boxes = boxes.copy()
                boxes[:, [0, 2]] = boxes[:, [0, 2]] * ratio[0] + padw
                boxes[:, [1, 3]] = boxes[:, [1, 3]] * ratio[1] + padh
                labels["instances"].boxes = boxes
            else:
                # torch.Tensor or similar
                boxes = boxes.clone()
                boxes[:, [0, 2]] = boxes[:, [0, 2]] * ratio[0] + padw
                boxes[:, [1, 3]] = boxes[:, [1, 3]] * ratio[1] + padh
                labels["instances"].boxes = boxes
        # Optionally update masks, keypoints, etc.
        if "instances" in labels and hasattr(labels["instances"], "masks"):
            masks = labels["instances"].masks
            if masks is not None:
                # Assume masks is a numpy array of shape (N, H, W)
                from skimage.transform import resize as sk_resize
                new_masks = []
                for mask in masks:
                    # Resize
                    mask_resized = cv2.resize(mask.astype(
                        np.float32), (0, 0), fx=ratio[0], fy=ratio[1], interpolation=cv2.INTER_NEAREST)
                    # Pad
                    mask_padded = np.pad(mask_resized, ((int(padh), 0), (int(
                        padw), 0)), mode='constant', constant_values=0)
                    # Crop to new shape if needed
                    new_masks.append(mask_padded)
                labels["instances"].masks = np.stack(new_masks, axis=0)
        if "instances" in labels and hasattr(labels["instances"], "keypoints"):
            keypoints = labels["instances"].keypoints
            if keypoints is not None:
                # keypoints: (N, K, 2)
                keypoints = keypoints.copy()
                keypoints[..., 0] = keypoints[..., 0] * ratio[0] + padw
                keypoints[..., 1] = keypoints[..., 1] * ratio[1] + padh
                labels["instances"].keypoints = keypoints
        return labels
