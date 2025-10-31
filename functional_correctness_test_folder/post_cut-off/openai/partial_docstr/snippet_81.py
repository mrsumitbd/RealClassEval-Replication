
import json
import os
from typing import Tuple, Union

import cv2
import numpy as np

try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    # fallback to TensorFlow Lite if tflite_runtime is not installed
    from tensorflow.lite.python.interpreter import Interpreter


class YOLOv8TFLite:
    def __init__(
        self,
        model: str,
        conf: float = 0.25,
        iou: float = 0.45,
        metadata: Union[str, None] = None,
    ):
        """
        Load a YOLOv8 TFLite model and optional metadata.

        Args:
            model (str): Path to the .tflite model file.
            conf (float): Confidence threshold for detections.
            iou (float): IoU threshold for non‑maximum suppression.
            metadata (str|None): Path to a JSON file mapping class IDs to names.
        """
        self.conf = conf
        self.iou = iou

        # Load the TFLite model
        self.interpreter = Interpreter(model_path=model)
        self.interpreter.allocate_tensors()

        # Get input details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Load metadata if provided
        self.class_names = {}
        if metadata and os.path.exists(metadata):
            with open(metadata, "r", encoding="utf-8") as f:
                self.class_names = json.load(f)

    def letterbox(
        self, img: np.ndarray, new_shape: Tuple = (640, 640)
    ) -> Tuple[np.ndarray, Tuple[float, float]]:
        """
        Resize image with unchanged aspect ratio using padding.

        Returns:
            padded image, (pad_top, pad_left)
        """
        shape = img.shape[:2]  # current shape [height, width]
        ratio = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        new_unpad = (int(round(shape[1] * ratio)),
                     int(round(shape[0] * ratio)))
        dw = new_shape[1] - new_unpad[0]
        dh = new_shape[0] - new_unpad[1]
        dw /= 2
        dh /= 2

        # Resize
        img_resized = cv2.resize(
            img, new_unpad, interpolation=cv2.INTER_LINEAR)

        # Pad
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img_padded = cv2.copyMakeBorder(
            img_resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(
                114, 114, 114)
        )

        return img_padded, (top, left)

    def draw_detections(
        self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int
    ) -> None:
        """
        Draw a single detection on the image.
        """
        h, w = img.shape[:2]
        x1, y1, x2, y2 = map(int, box)
        color = (0, 255, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        label = f"{self.class_names.get(str(class_id), str(class_id))}: {score:.2f}"
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        cv2.rectangle(
            img,
            (x1, y1 - t_size[1] - 4),
            (x1 + t_size[0], y1),
            color,
            -1,
        )
        cv2.putText(
            img,
            label,
            (x1, y1 - 2),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 0),
            1,
            cv2.LINE_AA,
        )

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        """
        Preprocess the image for inference.
        """
        img_resized, pad = self.letterbox(img, new_shape=(640, 640))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        img_norm = img_rgb.astype(np.float32) / 255.0
        img_batch = np.expand_dims(img_norm, axis=0)
        return img_batch, pad

    def postprocess(
        self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]
    ) -> np.ndarray:
        """
        Postprocess the model output and draw detections.
        """
        # outputs shape: [1, N, 6] -> [x1, y1, x2, y2, conf, cls_conf]
        detections = outputs[0]
        if detections.size == 0:
            return img

        # Compute scores
        scores = detections[:, 4] * detections[:, 5]
        mask = scores > self.conf
        detections = detections[mask]
        scores = scores[mask]

        if detections.size == 0:
            return img

        # Convert to boxes in original image scale
        pad_top, pad_left = pad
        scale = 640 / max(img.shape[:2])
        boxes = detections[:, :4]
        boxes[:, 0] -= pad_left
        boxes[:, 1] -= pad_top
        boxes[:, 2] -= pad_left
        boxes[:, 3] -= pad_top
        boxes /= scale

        # Clip boxes
        h, w = img.shape[:2]
        boxes[:, 0] = np.clip(boxes[:, 0], 0, w - 1)
        boxes[:, 1] = np.clip(boxes[:, 1], 0, h - 1)
        boxes[:, 2] = np.clip(boxes[:, 2], 0, w - 1)
        boxes[:, 3] = np.clip(boxes[:, 3], 0, h - 1)

        # NMS
        indices = cv2.dnn.NMSBoxes(
            boxes.tolist(), scores.tolist(), self.conf, self.iou
        )
        if len(indices) == 0:
            return img

        for i in indices.flatten():
            box = boxes[i]
            score = scores[i]
            class_id = int(detections[i, 5] * len(self.class_names))
            self.draw_detections(img, box, score, class_id)

        return img

    def detect(self, img_path: str) -> np.ndarray:
        """
        Run inference on an image file and return the image with detections.
        """
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"Image not found: {
