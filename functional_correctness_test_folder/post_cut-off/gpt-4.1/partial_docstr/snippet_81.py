
import numpy as np
import cv2
from typing import Tuple, Union
import tflite_runtime.interpreter as tflite
import json
import os


class YOLOv8TFLite:

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):
        self.model_path = model
        self.conf = conf
        self.iou = iou
        self.interpreter = tflite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_shape = self.input_details[0]['shape'][1:3]
        self.class_names = None
        if metadata is not None:
            if os.path.exists(metadata):
                with open(metadata, 'r') as f:
                    self.class_names = json.load(f)
            else:
                self.class_names = None

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
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label = f"{self.class_names[class_id] if self.class_names else class_id}: {score:.2f}"
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - 20), (x1 + w, y1), color, -1)
        cv2.putText(img, label, (x1, y1 - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        img0 = img.copy()
        img, (ratio, dw, dh) = self.letterbox(img0, self.input_shape)
        img = img.astype(np.float32)
        img /= 255.0
        img = np.expand_dims(img, axis=0)
        return img, (ratio, dw, dh)

    def nms(self, boxes, scores, iou_threshold):
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        areas = (x2 - x1) * (y2 - y1)
        order = scores.argsort()[::-1]
        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            w = np.maximum(0.0, xx2 - xx1)
            h = np.maximum(0.0, yy2 - yy1)
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter)
            inds = np.where(ovr <= iou_threshold)[0]
            order = order[inds + 1]
        return keep

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        ratio, dw, dh = pad
        if outputs.ndim == 3:
            outputs = outputs[0]
        boxes = outputs[:, :4]
        scores = outputs[:, 4]
        class_probs = outputs[:, 5:]
        class_ids = np.argmax(class_probs, axis=1)
        confidences = scores * \
            class_probs[np.arange(len(class_probs)), class_ids]
        mask = confidences > self.conf
        boxes = boxes[mask]
        confidences = confidences[mask]
        class_ids = class_ids[mask]
        if len(boxes) == 0:
            return img
        # Convert boxes from [cx, cy, w, h] to [x1, y1, x2, y2]
        boxes_xyxy = np.zeros_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2  # x1
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2  # y1
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2  # x2
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2  # y2
        # Undo letterbox
        boxes_xyxy[:, [0, 2]] -= dw
        boxes_xyxy[:, [1, 3]] -= dh
        boxes_xyxy /= ratio
        # NMS
        keep = self.nms(boxes_xyxy, confidences, self.iou)
        for i in keep:
            self.draw_detections(
                img, boxes_xyxy[i], confidences[i], class_ids[i])
        return img

    def detect(self, img_path: str) -> np.ndarray:
        img0 = cv2.imread(img_path)
        img_input, pad = self.preprocess(img0)
        input_index = self.input_details[0]['index']
        self.interpreter.set_tensor(input_index, img_input.astype(np.float32))
        self.interpreter.invoke()
        output_index = self.output_details[0]['index']
        outputs = self.interpreter.get_tensor(output_index)
        img_result = self.postprocess(img0, outputs, pad)
        return img_result
