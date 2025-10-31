
import numpy as np
from typing import Tuple, Union
import cv2
import tensorflow as tf


class YOLOv8TFLite:

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):

        self.model = tf.lite.Interpreter(model_path=model)
        self.model.allocate_tensors()
        self.input_details = self.model.get_input_details()
        self.output_details = self.model.get_output_details()
        self.conf = conf
        self.iou = iou
        self.metadata = metadata

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:

        shape = img.shape[:2]
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
        dw /= 2
        dh /= 2
        if shape[::-1] != new_unpad:
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
        return img, (top, left)

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:

        x1, y1, x2, y2 = box.astype(int)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{class_id}: {score:.2f}"
        cv2.putText(img, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:

        img, pad = self.letterbox(img)
        img = img.transpose((2, 0, 1))
        img = np.expand_dims(img, axis=0)
        img = img.astype(np.float32) / 255.0
        return img, pad

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:

        outputs = np.squeeze(outputs)
        outputs = outputs[outputs[:, 4] > self.conf]
        boxes = outputs[:, :4]
        scores = outputs[:, 4]
        class_ids = outputs[:, 5].astype(int)
        indices = cv2.dnn.NMSBoxes(
            boxes.tolist(), scores.tolist(), self.conf, self.iou)
        for i in indices:
            box = boxes[i]
            score = scores[i]
            class_id = class_ids[i]
            x1, y1, x2, y2 = box
            x1 -= pad[1]
            y1 -= pad[0]
            x2 -= pad[1]
            y2 -= pad[0]
            self.draw_detections(img, np.array(
                [x1, y1, x2, y2]), score, class_id)
        return img

    def detect(self, img_path: str) -> np.ndarray:

        img = cv2.imread(img_path)
        img, pad = self.preprocess(img)
        self.model.set_tensor(self.input_details[0]['index'], img)
        self.model.invoke()
        outputs = self.model.get_tensor(self.output_details[0]['index'])
        img = self.postprocess(img, outputs, pad)
        return img
