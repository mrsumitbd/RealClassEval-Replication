
import numpy as np
import cv2
from typing import Tuple, Union
import tflite_runtime.interpreter as tflite
import json


class YOLOv8TFLite:

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):
        self.model_path = model
        self.conf = conf
        self.iou = iou
        self.interpreter = tflite.Interpreter(model_path=model)
        self.interpreter.allocate_tensors()
        input_details = self.interpreter.get_input_details()
        self.input_index = input_details[0]['index']
        self.input_shape = input_details[0]['shape']
        self.input_height = self.input_shape[1]
        self.input_width = self.input_shape[2]
        output_details = self.interpreter.get_output_details()
        self.output_index = output_details[0]['index']
        self.metadata = None
        if metadata is not None:
            with open(metadata, 'r') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {"names": [str(i) for i in range(80)]}  # fallback

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        shape = img.shape[:2]  # current shape [height, width]
        ratio = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        new_unpad = (int(round(shape[1] * ratio)),
                     int(round(shape[0] * ratio)))
        dw = new_shape[1] - new_unpad[0]
        dh = new_shape[0] - new_unpad[1]
        dw /= 2
        dh /= 2
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
        return img, (ratio, dw, dh)

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:
        x1, y1, x2, y2 = box.astype(int)
        color = (0, 255, 0)
        label = f"{self.metadata['names'][class_id]} {score:.2f}"
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), color, -1)
        cv2.putText(img, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        img0 = img.copy()
        img, (ratio, dw, dh) = self.letterbox(
            img0, (self.input_height, self.input_width))
        img = img.astype(np.float32)
        img /= 255.0
        img = np.expand_dims(img, axis=0)
        return img, (ratio, dw, dh)

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        ratio, dw, dh = pad
        detections = []
        if outputs.shape[-1] == 6:
            # [N, 6]: x1, y1, x2, y2, score, class
            for det in outputs:
                x1, y1, x2, y2, score, class_id = det
                if score < self.conf:
                    continue
                # Undo letterbox
                x1 = (x1 - dw) / ratio
                y1 = (y1 - dh) / ratio
                x2 = (x2 - dw) / ratio
                y2 = (y2 - dh) / ratio
                x1 = np.clip(x1, 0, img.shape[1])
                y1 = np.clip(y1, 0, img.shape[0])
                x2 = np.clip(x2, 0, img.shape[1])
                y2 = np.clip(y2, 0, img.shape[0])
                detections.append([x1, y1, x2, y2, score, int(class_id)])
        else:
            # [N, 85]: x, y, w, h, conf, 80 class scores
            for det in outputs:
                scores = det[5:]
                class_id = np.argmax(scores)
                score = det[4] * scores[class_id]
                if score < self.conf:
                    continue
                x, y, w, h = det[:4]
                x1 = x - w / 2
                y1 = y - h / 2
                x2 = x + w / 2
                y2 = y + h / 2
                # Undo letterbox
                x1 = (x1 - dw) / ratio
                y1 = (y1 - dh) / ratio
                x2 = (x2 - dw) / ratio
                y2 = (y2 - dh) / ratio
                x1 = np.clip(x1, 0, img.shape[1])
                y1 = np.clip(y1, 0, img.shape[0])
                x2 = np.clip(x2, 0, img.shape[1])
                y2 = np.clip(y2, 0, img.shape[0])
                detections.append([x1, y1, x2, y2, score, int(class_id)])
        if len(detections) == 0:
            return np.zeros((0, 6))
        detections = np.array(detections)
        # NMS
        boxes = detections[:, :4]
        scores = detections[:, 4]
        class_ids = detections[:, 5]
        indices = cv2.dnn.NMSBoxes(
            bboxes=boxes.tolist(),
            scores=scores.tolist(),
            score_threshold=self.conf,
            nms_threshold=self.iou
        )
        if len(indices) == 0:
            return np.zeros((0, 6))
        indices = np.array(indices).flatten()
        return detections[indices]

    def detect(self, img_path: str) -> np.ndarray:
        img0 = cv2.imread(img_path)
        if img0 is None:
            raise FileNotFoundError(f"Image not found: {img_path}")
        img, pad = self.preprocess(img0)
        self.interpreter.set_tensor(self.input_index, img)
        self.interpreter.invoke()
        output = self.interpreter.get_tensor(self.output_index)
        if output.ndim == 3:
            output = output[0]
        detections = self.postprocess(img0, output, pad)
        for det in detections:
            box = det[:4]
            score = det[4]
            class_id = int(det[5])
            self.draw_detections(img0, box, score, class_id)
        return img0
