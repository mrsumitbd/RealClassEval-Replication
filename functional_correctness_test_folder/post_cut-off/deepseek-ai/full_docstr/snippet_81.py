
import numpy as np
import cv2
import tensorflow as tf
from typing import Tuple, Union


class YOLOv8TFLite:
    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):
        self.model = model
        self.conf = conf
        self.iou = iou
        self.metadata = metadata
        self.interpreter = tf.lite.Interpreter(model_path=self.model)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        shape = img.shape[:2]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)
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
        return img, (dh, dw)

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:
        x1, y1, w, h = box
        x1, y1, x2, y2 = int(x1), int(y1), int(x1 + w), int(y1 + h)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f"{class_id}: {score:.2f}"
        cv2.putText(img, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        img, pad = self.letterbox(img)
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)
        return img, pad

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        dh, dw = pad
        original_shape = img.shape[:2]
        outputs = np.squeeze(outputs)
        boxes = outputs[:, :4]
        scores = outputs[:, 4]
        class_ids = outputs[:, 5].astype(int)
        boxes[:, 0] = (boxes[:, 0] - dw) / (1 - 2 * dw) * original_shape[1]
        boxes[:, 1] = (boxes[:, 1] - dh) / (1 - 2 * dh) * original_shape[0]
        boxes[:, 2] = boxes[:, 2] / (1 - 2 * dw) * original_shape[1]
        boxes[:, 3] = boxes[:, 3] / (1 - 2 * dh) * original_shape[0]
        indices = cv2.dnn.NMSBoxes(
            boxes.tolist(), scores.tolist(), self.conf, self.iou)
        for i in indices:
            box = boxes[i]
            score = scores[i]
            class_id = class_ids[i]
            self.draw_detections(img, box, score, class_id)
        return img

    def detect(self, img_path: str) -> np.ndarray:
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Image not found at {img_path}")
        input_img, pad = self.preprocess(img)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_img)
        self.interpreter.invoke()
        outputs = self.interpreter.get_tensor(self.output_details[0]['index'])
        output_img = self.postprocess(img, outputs, pad)
        return output_img
