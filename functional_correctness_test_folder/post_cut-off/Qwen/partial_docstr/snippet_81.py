
import numpy as np
import cv2
from typing import Union, Tuple


class YOLOv8TFLite:

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):
        self.model = cv2.dnn.readNet(model)
        self.conf = conf
        self.iou = iou
        self.metadata = metadata
        self.classes = self._load_classes() if metadata else []

    def _load_classes(self) -> list:
        with open(self.metadata, 'r') as f:
            return [line.strip() for line in f.readlines()]

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        h, w = img.shape[:2]
        r = min(new_shape[0] / h, new_shape[1] / w)
        new_unpad = int(round(w * r)), int(round(h * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
        dw /= 2
        dh /= 2
        if img.size != new_unpad:
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
        return img, (top, left)

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:
        color = (int(255 * np.random.rand()), int(255 *
                 np.random.rand()), int(255 * np.random.rand()))
        c1, c2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
        cv2.rectangle(img, c1, c2, color, 3)
        label = f'{self.classes[class_id]} {score:.2f}'
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(img, c1, (c1[0] + w, c1[1] -
                      h - 3), color, -1, cv2.LINE_AA)
        cv2.putText(img, label, (c1[0], c1[1] - 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        img, pad = self.letterbox(img)
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img)
        img = img.astype(np.float32) / 255.0
        return img, pad

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        h, w = img.shape[:2]
        top, left = pad
        boxes = []
        scores = []
        class_ids = []
        for output in outputs:
            for detection in output:
                scores_data = detection[4:]
                class_id = np.argmax(scores_data)
                confidence = scores_data[class_id]
                if confidence > self.conf:
                    box = detection[:4]
                    box[0] -= left
                    box[2] -= left
                    box[1] -= top
                    box[3] -= top
                    box[0] /= w
                    box[2] /= w
                    box[1] /= h
                    box[3] /= h
                    (centerX, centerY, width, height) = box.astype("float")
                    x = int(centerX * w)
                    y = int(centerY * h)
                    x1 = int(x - (width * w) / 2)
                    y1 = int(y - (height * h) / 2)
                    x2 = int(x + (width * w) / 2)
                    y2 = int(y + (height * h) / 2)
                    boxes.append([x1, y1, x2, y2])
                    scores.append(float(confidence))
                    class_ids.append(class_id)
        indices = cv2.dnn.NMSBoxes(boxes, scores, self.conf, self.iou)
        for i in indices:
            i = i[0]
            box = boxes[i]
            score = scores[i]
            class_id = class_ids[i]
            self.draw_detections(img, box, score, class_id)
        return img

    def detect(self, img_path: str) -> np.ndarray:
        img = cv2.imread(img_path)
        blob, pad = self.preprocess(img)
        blob = np.expand_dims(blob, 0)
        self.model.setInput(blob)
        outputs = self.model.forward(self.model.getUnconnectedOutLayersNames())
        img = self.postprocess(img, outputs, pad)
        return img
