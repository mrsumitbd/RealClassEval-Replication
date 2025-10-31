
import numpy as np
from typing import Tuple, Union
import cv2
import tensorflow as tf
from PIL import Image


class YOLOv8TFLite:

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):
        self.interpreter = tf.lite.Interpreter(model_path=model)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.conf_threshold = conf
        self.iou_threshold = iou
        self.class_names = []
        if metadata:
            with open(metadata, 'r') as f:
                self.class_names = [line.strip() for line in f.readlines()]

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        shape = img.shape[:2]
        ratio = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        new_unpad = (int(round(shape[1] * ratio)),
                     int(round(shape[0] * ratio)))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
        dw, dh = dw / 2, dh / 2
        if shape[::-1] != new_unpad:
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
        return img, (dw, dh)

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:
        x1, y1, x2, y2 = box.astype(int)
        color = (0, 255, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label = f"{self.class_names[class_id]}: {score:.2f}"
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), color, -1)
        cv2.putText(img, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        img, pad = self.letterbox(img)
        img = img[:, :, ::-1].transpose(2, 0, 1)
        img = np.ascontiguousarray(img, dtype=np.float32)
        img /= 255.0
        return img, pad

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        dw, dh = pad
        rows = outputs[0].shape[0]
        boxes, scores, class_ids = [], [], []
        for i in range(rows):
            output = outputs[0][i]
            score = output[4]
            if score < self.conf_threshold:
                continue
            class_id = np.argmax(output[5:])
            x, y, w, h = output[0], output[1], output[2], output[3]
            x1 = int((x - w / 2 - dw) * img.shape[1] / (640 - 2 * dw))
            y1 = int((y - h / 2 - dh) * img.shape[0] / (640 - 2 * dh))
            x2 = int((x + w / 2 - dw) * img.shape[1] / (640 - 2 * dw))
            y2 = int((y + h / 2 - dh) * img.shape[0] / (640 - 2 * dh))
            boxes.append([x1, y1, x2, y2])
            scores.append(score)
            class_ids.append(class_id)
        indices = cv2.dnn.NMSBoxes(
            boxes, scores, self.conf_threshold, self.iou_threshold)
        for i in indices:
            self.draw_detections(img, np.array(
                boxes[i]), scores[i], class_ids[i])
        return img

    def detect(self, img_path: str) -> np.ndarray:
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        input_img, pad = self.preprocess(img_rgb)
        input_img = np.expand_dims(input_img, axis=0)
        self.interpreter.set_tensor(self.input_details[0]['index'], input_img)
        self.interpreter.invoke()
        outputs = [self.interpreter.get_tensor(
            output_detail['index']) for output_detail in self.output_details]
        result = self.postprocess(img, outputs, pad)
        return result
