
import numpy as np
from typing import Tuple, Union
import cv2
import tensorflow as tf
from tensorflow.lite.python.interpreter import Interpreter


class YOLOv8TFLite:

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):
        self.conf = conf
        self.iou = iou
        self.interpreter = Interpreter(model_path=model)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_shape = self.input_details[0]['shape'][1:3]
        self.class_names = []
        if metadata:
            with open(metadata, 'r') as f:
                self.class_names = [line.strip() for line in f.readlines()]

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
        return img, (dh, dw)

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:
        x1, y1, x2, y2 = box.astype(int)
        color = (0, 255, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label = f"{self.class_names[class_id]}: {score:.2f}"
        cv2.putText(img, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        img_resized, pad = self.letterbox(img, self.input_shape)
        img_resized = img_resized.astype(np.float32) / 255.0
        img_resized = np.expand_dims(img_resized, axis=0)
        return img_resized, pad

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        dh, dw = pad
        img_height, img_width = img.shape[:2]
        boxes = outputs[:, :4]
        scores = outputs[:, 4]
        class_ids = outputs[:, 5].astype(int)

        for box, score, class_id in zip(boxes, scores, class_ids):
            if score < self.conf:
                continue
            x1, y1, x2, y2 = box
            x1 = int((x1 - dw) * img_width / self.input_shape[1])
            y1 = int((y1 - dh) * img_height / self.input_shape[0])
            x2 = int((x2 - dw) * img_width / self.input_shape[1])
            y2 = int((y2 - dh) * img_height / self.input_shape[0])
            self.draw_detections(img, np.array(
                [x1, y1, x2, y2]), score, class_id)
        return img

    def detect(self, img_path: str) -> np.ndarray:
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Image not found at {img_path}")
        img_preprocessed, pad = self.preprocess(img)
        self.interpreter.set_tensor(
            self.input_details[0]['index'], img_preprocessed)
        self.interpreter.invoke()
        outputs = self.interpreter.get_tensor(self.output_details[0]['index'])
        return self.postprocess(img.copy(), outputs, pad)
