
import numpy as np
import cv2
from typing import Union, Tuple
import tensorflow as tf


class YOLOv8TFLite:

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):
        self.model = tf.lite.Interpreter(model_path=model)
        self.model.allocate_tensors()
        self.conf = conf
        self.iou = iou
        self.metadata = metadata
        self.input_details = self.model.get_input_details()
        self.output_details = self.model.get_output_details()

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        h, w = img.shape[:2]
        r = min(new_shape[0] / h, new_shape[1] / w)
        new_unpad = int(round(w * r)), int(round(h * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
        dw, dh = dw / 2, dh / 2
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
        return img, (dw / w, dh / h)

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:
        x1, y1, x2, y2 = box.astype(int)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f'{class_id}: {score:.2f}'
        cv2.putText(img, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        img, pad = self.letterbox(img)
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)
        return img, pad

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        boxes, scores, classes = outputs
        h, w = img.shape[:2]
        dw, dh = pad
        boxes[:, 0] -= dw
        boxes[:, 2] -= dw
        boxes[:, 1] -= dh
        boxes[:, 3] -= dh
        boxes[:, 0] /= (1 - dw * 2)
        boxes[:, 2] /= (1 - dw * 2)
        boxes[:, 1] /= (1 - dh * 2)
        boxes[:, 3] /= (1 - dh * 2)
        boxes[:, 0] *= w
        boxes[:, 2] *= w
        boxes[:, 1] *= h
        boxes[:, 3] *= h
        return np.concatenate((boxes, scores[:, np.newaxis], classes[:, np.newaxis]), axis=1)

    def detect(self, img_path: str) -> np.ndarray:
        img = cv2.imread(img_path)
        img_preprocessed, pad = self.preprocess(img)
        self.model.set_tensor(self.input_details[0]['index'], img_preprocessed)
        self.model.invoke()
        outputs = [self.model.get_tensor(
            self.output_details[i]['index']) for i in range(len(self.output_details))]
        detections = self.postprocess(img, outputs, pad)
        for detection in detections:
            box, score, class_id = detection[:4], detection[4], int(
                detection[5])
            if score > self.conf:
                self.draw_detections(img, box, score, class_id)
        return img
