
import numpy as np


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
        if image is None:
            image = labels.get('img')

        shape = image.shape[:2]  # current shape [height, width]
        new_shape = self.new_shape

        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        if not self.scaleup:
            r = min(r, 1.0)

        # Compute padding
        ratio = r, r
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]

        if self.scaleFill:
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]

        if self.center:
            dw /= 2
            dh /= 2

        if shape[::-1] != new_unpad:
            image = cv2.resize(
                image, new_unpad, interpolation=cv2.INTER_LINEAR)

        top, bottom = int(
            round(dh - 0.1)) if self.center else 0, int(round(dh + 0.1))
        left, right = int(
            round(dw - 0.1)) if self.center else 0, int(round(dw + 0.1))
        image = cv2.copyMakeBorder(
            image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))

        if len(labels):
            labels = self._update_labels(labels, ratio, dw, dh)
            labels['img'] = image
            labels['resized_shape'] = new_shape
            return labels
        else:
            return image, (ratio, (dw, dh))

    @staticmethod
    def _update_labels(labels, ratio, padw, padh):
        if 'instances' in labels:
            instances = labels['instances']
            bboxes = instances.get('bboxes')
            if bboxes is not None:
                bboxes[:, 0] = ratio[0] * bboxes[:, 0] + padw
                bboxes[:, 1] = ratio[1] * bboxes[:, 1] + padh
                bboxes[:, 2] = ratio[0] * bboxes[:, 2] + padw
                bboxes[:, 3] = ratio[1] * bboxes[:, 3] + padh
                instances['bboxes'] = bboxes
            labels['instances'] = instances
        return labels
