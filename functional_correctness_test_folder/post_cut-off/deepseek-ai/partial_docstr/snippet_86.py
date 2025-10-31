
import numpy as np
from typing import Dict, Tuple, Optional, Union


class LetterBox:
    def __init__(self, new_shape=(640, 640), auto=False, scaleFill=False, scaleup=True, center=True, stride=32):
        self.new_shape = new_shape
        self.auto = auto
        self.scaleFill = scaleFill
        self.scaleup = scaleup
        self.stride = stride
        self.center = center

    def __call__(self, labels=None, image=None):
        if labels is None:
            labels = {}
        img = labels.get('img') if image is None else image
        shape = img.shape[:2]  # current shape [height, width]
        new_shape = self.new_shape

        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        # only scale down, do not scale up (for better val mAP)
        if not self.scaleup:
            r = min(r, 1.0)

        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - \
            new_unpad[1]  # wh padding

        if self.auto:  # minimum rectangle
            dw, dh = np.mod(dw, self.stride), np.mod(
                dh, self.stride)  # wh padding
        elif self.scaleFill:  # stretch
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = new_shape[1] / shape[1], new_shape[0] / \
                shape[0]  # width, height ratios

        if self.center:
            dw /= 2  # divide padding into 2 sides
            dh /= 2

        if shape[::-1] != new_unpad:  # resize
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(
            dh - 0.1)) if self.center else 0, int(round(dh + 0.1)) if self.center else dh
        left, right = int(round(
            dw - 0.1)) if self.center else 0, int(round(dw + 0.1)) if self.center else dw
        img = cv2.copyMakeBorder(img, top, bottom, left, right,
                                 cv2.BORDER_CONSTANT, value=(114, 114, 114))  # add border

        if len(labels):
            labels = self._update_labels(labels, ratio, (left, top))
            labels['img'] = img
            labels['resized_shape'] = new_shape
            return labels
        else:
            return img, (ratio, (left, top))

    @staticmethod
    def _update_labels(labels, ratio, pad):
        """Update labels after applying letterboxing."""
        instances = labels.get('instances')
        if instances is None:
            return labels

        # Update bounding boxes
        if hasattr(instances, 'bboxes'):
            instances.bboxes[:, [0, 2]] = instances.bboxes[:,
                                                           [0, 2]] * ratio[0] + pad[0]  # x padding
            instances.bboxes[:, [1, 3]] = instances.bboxes[:,
                                                           [1, 3]] * ratio[1] + pad[1]  # y padding

        # Update keypoints if they exist
        if hasattr(instances, 'keypoints'):
            keypoints = instances.keypoints
            if keypoints is not None and len(keypoints):
                keypoints[..., 0] = keypoints[..., 0] * \
                    ratio[0] + pad[0]  # x padding
                keypoints[..., 1] = keypoints[..., 1] * \
                    ratio[1] + pad[1]  # y padding

        # Update segments if they exist
        if hasattr(instances, 'segments'):
            segments = instances.segments
            if segments is not None and len(segments):
                segments[..., 0] = segments[..., 0] * \
                    ratio[0] + pad[0]  # x padding
                segments[..., 1] = segments[..., 1] * \
                    ratio[1] + pad[1]  # y padding

        return labels
