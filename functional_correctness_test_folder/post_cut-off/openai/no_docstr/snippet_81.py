
import cv2
import numpy as np
from typing import Tuple, Union, List
import tflite_runtime.interpreter as tflite
import os


class YOLOv8TFLite:
    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):
        """
        Initialize the YOLOv8 TFLite detector.

        Parameters
        ----------
        model : str
            Path to the TFLite model file.
        conf : float, optional
            Confidence threshold for detections.
        iou : float, optional
            IoU threshold for non‑maximum suppression.
        metadata : str or None, optional
            Path to a text file containing class names (one per line).
        """
        self.conf_thresh = conf
        self.iou_thresh = iou

        # Load class names if metadata is provided
        self.class_names: List[str] = []
        if metadata is not None:
            if os.path.isfile(metadata):
                with open(metadata, "r", encoding="utf-8") as f:
                    self.class_names = [line.strip() for line in f.readlines()]
            else:
                raise FileNotFoundError(f"Metadata file not found: {metadata}")

        # Load TFLite model
        self.interpreter = tflite.Interpreter(model_path=model)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        """
        Resize image with unchanged aspect ratio using padding.

        Parameters
        ----------
        img : np.ndarray
            Input image.
        new_shape : Tuple, optional
            Desired shape (height, width).

        Returns
        -------
        Tuple[np.ndarray, Tuple[float, float]]
            Resized image and (scale, pad) used for later coordinate conversion.
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
        img_padded = cv2.copyMakeBorder(img_resized, top, bottom, left, right,
                                        cv2.BORDER_CONSTANT, value=(114, 114, 114))

        return img_padded, (ratio, (dw, dh))

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:
        """
        Draw a single detection on the image.

        Parameters
        ----------
        img : np.ndarray
            Image to draw on.
        box : np.ndarray
            Bounding box [x1, y1, x2, y2].
        score : np.float32
            Confidence score.
        class_id : int
            Class index.
        """
        x1, y1, x2, y2 = map(int, box)
        color = (0, 255, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label = f"{self.class_names[class_id] if self.class_names else class_id}: {score:.2f}"
        t_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        cv2.rectangle(
            img, (x1, y1 - t_size[1] - 4), (x1 + t_size[0], y1), color, -1)
        cv2.putText(img, label, (x1, y1 - 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        """
        Preprocess image for YOLOv8 TFLite model.

        Parameters
        ----------
        img : np.ndarray
            Input image.

        Returns
        -------
        Tuple[np.ndarray, Tuple[float, float]]
            Preprocessed image and padding info.
        """
        img_resized, pad = self.letterbox(img, new_shape=(640, 640))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
        img_norm = img_rgb.astype(np.float32) / 255.0
        img_batch = np.expand_dims(img_norm, axis=0)
        return img_batch, pad

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        """
        Postprocess model outputs and draw detections.

        Parameters
        ----------
        img : np.ndarray
            Original image.
        outputs : np.ndarray
            Model output tensor.
        pad : Tuple[float, float]
            Padding info from preprocessing.

        Returns
        -------
        np.ndarray
            Image with detections drawn.
        """
        # YOLOv8 TFLite output shape: [1, N, 6] -> [x, y, w, h, conf, cls]
        detections = outputs[0]  # shape (N, 6)
        boxes = []
        scores = []
        class_ids = []

        ratio, (dw, dh) = pad
        for det in detections:
            cx, cy, w, h, conf, cls = det
            if conf < self.conf_thresh:
                continue
            # Convert to corner coordinates
            x1 = int((cx - w / 2) * ratio)
            y1 = int((cy - h / 2) * ratio)
            x2 = int((cx + w / 2) * ratio)
            y2 = int((cy + h / 2) * ratio)
            # cv2.dnn.NMSBoxes expects [x, y, w, h]
            boxes.append([x1, y1, x2 - x1, y2 - y1])
            scores.append(float(conf))
            class_ids.append(int(cls))

        # Apply NMS
        indices = cv2.dnn.NMSBoxes(
            boxes, scores, self.conf_thresh, self.iou_thresh)
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w_box, h_box = boxes[i]
                x1, y1 = x, y
                x2, y2 = x + w_box, y + h_box
                self.draw_detections(img, np.array(
                    [x1, y1, x2, y2]), scores[i], class_ids[i])

        return img

    def detect(self, img_path: str) -> np.ndarray:
        """
        Run detection on an image file.

        Parameters
        ----------
        img_path : str
            Path to the image file.

        Returns
        -------
