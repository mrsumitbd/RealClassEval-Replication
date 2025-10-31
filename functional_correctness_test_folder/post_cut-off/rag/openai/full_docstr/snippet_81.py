
import json
import os
from pathlib import Path
from typing import Tuple, Union

import cv2
import numpy as np

try:
    # tflite_runtime is lighter than full TensorFlow
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    # fallback to TensorFlow Lite
    from tensorflow.lite.python.interpreter import Interpreter


class YOLOv8TFLite:
    """
    YOLOv8TFLite.
    A class for performing object detection using the YOLOv8 model with TensorFlow Lite.
    """

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45,
                 metadata: Union[str, None] = None):
        """
        Initializes an instance of the YOLOv8TFLite class.
        """
        self.model_path = Path(model)
        if not self.model_path.is_file():
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        self.conf = conf
        self.iou = iou
        self.metadata = Path(metadata) if metadata else None
        self.class_names = []

        if self.metadata and self.metadata.is_file():
            with open(self.metadata, "r", encoding="utf-8") as f:
                data = json.load(f)
                # YOLOv8 metadata format: {"names": {"0": "person", ...}}
                if "names" in data:
                    # ensure list order
                    self.class_names = [
                        data["names"][str(i)] for i in range(len(data["names"]))]
                else:
                    # fallback: assume list
                    self.class_names = data

        # Load TFLite model
        self.interpreter = Interpreter(model_path=str(self.model_path))
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Input shape
        self.input_shape = tuple(self.input_details[0]["shape"][1:3])  # (H, W)

    def letterbox(self, img: np.ndarray,
                  new_shape: Tuple[int, int] = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        """
        Resizes and reshapes images while maintaining aspect ratio by adding padding,
        suitable for YOLO models.
        """
        shape = img.shape[:2]  # current shape [height, width]
        ratio = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        new_unpad = (int(round(shape[1] * ratio)),
                     int(round(shape[0] * ratio)))
        dw = new_shape[1] - new_unpad[0]
        dh = new_shape[0] - new_unpad[1]
        dw /= 2
        dh /= 2

        # resize
        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)

        # pad
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(img, top, bottom, left, right,
                                 cv2.BORDER_CONSTANT, value=(114, 114, 114))

        return img, (dw, dh)

    def draw_detections(self, img: np.ndarray, box: np.ndarray,
                        score: np.float32, class_id: int) -> None:
        """
        Draws bounding boxes and labels on the input image based on the detected objects.
        """
        x1, y1, w, h = box
        x2, y2 = int(x1 + w), int(y1 + h)
        color = (0, 255, 0)  # green
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        label = f"{self.class_names[class_id] if self.class_names else class_id}: {score:.2f}"
        (text_w, text_h), _ = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - text_h - 4), (x1 + text_w, y1), color, -1)
        cv2.putText(img, label, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        """
        Preprocesses the input image before performing inference.
        """
        img_resized, pad = self.letterbox(img, new_shape=self.input_shape)
        img_resized = img_resized.astype(np.float32) / 255.0
        # TFLite expects NHWC
        img_resized = np.expand_dims(img_resized, axis=0)
        return img_resized, pad

    def _nms(self, boxes, scores, iou_threshold):
        """
        Simple NMS implementation.
        """
        idxs = np.argsort(scores)[::-1]
        keep = []
        while len(idxs) > 0:
            i = idxs[0]
            keep.append(i)
            if len(idxs) == 1:
                break
            rest = idxs[1:]
            i_box = boxes[i]
            rest_boxes = boxes[rest]
            xx1 = np.maximum(i_box[0], rest_boxes[:, 0])
            yy1 = np.maximum(i_box[1], rest_boxes[:, 1])
            xx2 = np.minimum(i_box[2], rest_boxes[:, 2])
            yy2 = np.minimum(i_box[3], rest_boxes[:, 3])

            w = np.maximum(0, xx2 - xx1)
            h = np.maximum(0, yy2 - yy1)
            inter = w * h
            area_i = (i_box[2] - i_box[0]) * (i_box[3] - i_box[1])
            area_rest = (rest_boxes[:, 2] - rest_boxes[:, 0]) * \
                         (rest_boxes[:, 3] - rest_boxes[:, 1])
            iou = inter / (area_i + area_rest - inter)

            idxs = idxs[1:][iou <= iou_threshold]
        return keep

    def postprocess(self, img: np.ndarray, outputs: np.ndarray,
                    pad: Tuple[float, float]) -> np.ndarray:
        """
        Performs post-processing on the model's output to extract bounding boxes,
        scores, and class IDs.
        """
        # outputs shape: [1, N, 6] -> [x, y, w, h, conf, cls]
        detections = outputs[0]  # shape (N, 6)
        # filter by confidence
        conf_mask = detections[:, 4] > self.conf
        detections = detections[conf_mask]
        if detections.size == 0:
            return img

        # convert to corner format
        boxes = detections[:, :4]
        scores = detections[:, 4] * detections[:, 5]  # confidence * class_prob
        class_ids = np.argmax(detections[:, 5:], axis=1)

        # scale boxes back to original image
        dw, dh = pad
        scale = min(self.input_shape[1] / img.shape[1],
                    self.input_shape[0] / img.shape[0])
        boxes[:,
