
import numpy as np


class LetterBox:
    def __init__(self, new_shape=(640, 640), auto=False, scaleFill=False, scaleup=True, center=True, stride=32):
        self.new_shape = new_shape
        self.auto = auto
        self.scaleFill = scaleFill
        self.scaleup = scaleup
        self.center = center
        self.stride = stride

    def __call__(self, labels=None, image=None):
        if labels is not None and "img" in labels:
            image = labels["img"]

        if image is None:
            raise ValueError(
                "Image must be provided either directly or within the labels dictionary.")

        shape = image.shape[:2]  # current shape [height, width]
        r = min(self.new_shape[0] / shape[0], self.new_shape[1] / shape[1])
        # only scale down, do not scale up (for better test mAP)
        if not self.scaleup:
            r = min(r, 1.0)

        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        # wh padding
        dw, dh = self.new_shape[1] - \
            new_unpad[0], self.new_shape[0] - new_unpad[1]

        if self.auto:  # minimum rectangle
            dw, dh = np.mod(dw, self.stride), np.mod(
                dh, self.stride)  # wh padding
        elif self.scaleFill:  # stretch
            dw, dh = 0.0, 0.0
            new_unpad = (self.new_shape[1], self.new_shape[0])
            # width, height ratios
            ratio = self.new_shape[1] / shape[1], self.new_shape[0] / shape[0]

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if self.center:
            top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
            left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        else:
            top, bottom = int(round(dh)), int(round(dh))
            left, right = int(round(dw)), int(round(dw))

        if image.shape[2] == 4:
            image = cv2.copyMakeBorder(
                image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(0, 0, 0, 0))  # add border
        else:
            image = cv2.copyMakeBorder(
                image, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))  # add border

        if labels is not None:
            labels = self._update_labels(labels, ratio, dw, dh)
            return {"img": image, "instances": labels["instances"]}
        else:
            return image, (ratio, (dw, dh))

    @staticmethod
    def _update_labels(labels, ratio, padw, padh):
        instances = labels["instances"]
        boxes = instances.boxes.tensor
        boxes[:, [0, 2]] = boxes[:, [0, 2]] * ratio[0] + padw
        boxes[:, [1, 3]] = boxes[:, [1, 3]] * ratio[1] + padh
        instances.boxes.tensor = boxes
        return labels
