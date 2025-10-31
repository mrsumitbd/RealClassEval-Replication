
import json
import os
from typing import Tuple, Union

import cv2
import numpy as np

try:
    from tflite_runtime.interpreter import Interpreter
except Exception:  # pragma: no cover
    # fallback to tensorflow if tflite_runtime is not installed
    import tensorflow as tf

    Interpreter = tf.lite.Interpreter


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
        self.model_path = model
        self.conf = conf
        self.iou = iou
        self.metadata_path = metadata
        self.class_names = None

        # Load class names if metadata is provided
        if self.metadata_path and os.path.exists(self.metadata_path):
            with open(self.metadata_path, "r") as f:
                meta = json.load(f)
                self.class_names = meta.get("names", None)

        # Load TFLite model
        self.interpreter = Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()

        # Input details
        self.input_details = self.interpreter.get_input_details()
        self.input_shape = self.input_details[0]["shape"]  # [1, H, W, 3]
        self.input_dtype = self.input_details[0]["dtype"]

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
        color = (0, 255, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        label = f"{self.class_names[class_id] if self.class_names else class_id}: {score:.2f}"
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        cv2.rectangle(
            img, (x1, y1 - t_size[1] - 4), (x1 + t_size[0], y1), color, -1)
        cv2.putText(img, label, (x1, y1 - 2), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        """
        Preprocesses the input image before performing inference.
        """
        img_resized, pad = self.letterbox(
            img, (self.input_shape[1], self.input_shape[2]))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        img_norm = img_rgb.astype(np.float32) / 255.0
        img_batch = np.expand_dims(img_norm, axis=0).astype(self.input_dtype)
        return img_batch, pad

    def postprocess(self, img: np.ndarray, outputs: np.ndarray,
                    pad: Tuple[float, float]) -> np.ndarray:
        """
        Performs post-processing on the model's output to extract bounding boxes,
        scores, and class IDs.
        """
        # YOLOv8 output shape: [1, N, 85] where 85 = 4 + 1 + 80
        preds = outputs[0]  # shape [N, 85]
        # sigmoid for objectness and class scores
        obj_conf = 1 / (1 + np.exp(-preds[:, 4]))
        class_conf = 1 / (1 + np.exp(-preds[:, 5:]))
        scores = obj_conf[:, None] * class_conf  # shape [N, 80]
        class_ids = np.argmax(scores, axis=1)
        class_scores = scores[np.arange(len(scores)), class_ids]

        # filter by confidence
        mask = class_scores > self.conf
        boxes = preds[mask, :4]
        scores = class_scores[mask]
        class_ids = class_ids[mask]

        # convert to xyxy
        boxes_xyxy = np.zeros_like(boxes)
        boxes_xyxy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2
        boxes_xyxy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2
        boxes_xyxy[:, 2] = boxes[:, 0] + boxes[:, 2] / 2
        boxes_xyxy[:, 3] = boxes[:, 1] + boxes[:, 3] / 2

        # undo padding and scaling
        dw, dh = pad
        boxes_xyxy[:, [0, 2]] -= dw
        boxes_xyxy[:, [1, 3]] -= dh
        boxes_xyxy /= self.input_shape[1] / 640  # scale factor

        # clip boxes
        h, w = img.shape[:2]
        boxes_xyxy[:, 0] = np.clip(boxes_xyxy[:, 0], 0, w - 1)
        boxes_xyxy[:, 1] = np.clip(boxes_xyxy[:, 1], 0, h - 1)
        boxes_xyxy[:, 2] = np.clip(boxes_xyxy[:, 2], 0, w - 1)
        boxes_xyxy[:, 3] = np.clip(boxes_xyxy[:, 3], 0, h - 1)

        # NMS
        indices = cv2.dnn.NMSBoxes(
            boxes_xyxy.tolist(),
            scores.tolist(),
            self.conf,
            self.iou
        )
        if len(indices) > 0:
            for i in indices.flatten():
                box = boxes_xyxy[i]
