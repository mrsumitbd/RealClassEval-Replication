
import cv2
import numpy as np
import json
import os
from typing import Tuple, Union, List, Optional

# Try to import tflite_runtime, fallback to tensorflow.lite
try:
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    from tensorflow.lite.python.interpreter import Interpreter


class YOLOv8TFLite:
    '''
    YOLOv8TFLite.
    A class for performing object detection using the YOLOv8 model with TensorFlow Lite.
    Attributes:
        model (str): Path to the TensorFlow Lite model file.
        conf (float): Confidence threshold for filtering detections.
        iou (float): Intersection over Union threshold for non-maximum suppression.
        metadata (Optional[str]): Path to the metadata file, if any.
    Methods:
        detect(img_path: str) -> np.ndarray:
            Performs inference and returns the output image with drawn detections.
    '''

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45,
                 metadata: Union[str, None] = None):
        '''
        Initializes an instance of the YOLOv8TFLite class.
        Args:
            model (str): Path to the TFLite model.
            conf (float, optional): Confidence threshold for filtering detections. Defaults to 0.25.
            iou (float, optional): IoU (Intersection over Union) threshold for non-maximum suppression. Defaults to 0.45.
            metadata (Union[str, None], optional): Path to the metadata file or None if not used. Defaults to None.
        '''
        self.model_path = model
        self.conf = conf
        self.iou = iou
        self.metadata_path = metadata
        self.class_names = self._load_metadata(metadata)

        # Load interpreter
        self.interpreter = Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_index = self.input_details[0]['index']
        # e.g., [1, 640, 640, 3]
        self.input_shape = self.input_details[0]['shape']
        self.input_dtype = self.input_details[0]['dtype']

    def _load_metadata(self, path: Optional[str]) -> List[str]:
        if path is None or not os.path.exists(path):
            return []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'names' in data:
                    return data['names']
                if isinstance(data, list):
                    return data
        except Exception:
            pass
        return []

    def letterbox(self, img: np.ndarray,
                  new_shape: Tuple[int, int] = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        '''Resizes and reshapes images while maintaining aspect ratio by adding padding, suitable for YOLO models.'''
        shape = img.shape[:2]  # current shape [height, width]
        ratio = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        # new width, height
        new_unpad = (int(round(shape[1] * ratio)),
                     int(round(shape[0] * ratio)))
        dw = new_shape[1] - new_unpad[0]
        dh = new_shape[0] - new_unpad[1]
        dw /= 2
        dh /= 2

        # resize
        img_resized = cv2.resize(
            img, new_unpad, interpolation=cv2.INTER_LINEAR)

        # pad
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img_padded = cv2.copyMakeBorder(img_resized, top, bottom, left, right,
                                        cv2.BORDER_CONSTANT, value=(114, 114, 114))
        return img_padded, (dw, dh)

    def draw_detections(self, img: np.ndarray, box: np.ndarray,
                        score: np.float32, class_id: int) -> None:
        '''
        Draws bounding boxes and labels on the input image based on the detected objects.
        Args:
            img (np.ndarray): The input image to draw detections on.
            box (np.ndarray): Detected bounding box in the format [x1, y1, width, height].
            score (np.float32): Corresponding detection score.
            class_id (int): Class ID for the detected object.
        Returns:
            None
        '''
        x1, y1, w, h = box
        x2, y2 = int(x1 + w), int(y1 + h)
        color = (0, 255, 0)
        cv2.rectangle(img, (int(x1), int(y1)), (x2, y2), color, 2)
        label = f'{self.class_names[class_id] if self.class_names else class_id}: {score:.2f}'
        cv2.putText(img, label, (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        '''
        Preprocesses the input image before performing inference.
        Args:
            img (np.ndarray): The input image to be preprocessed.
        Returns:
            Tuple[np.ndarray, Tuple[float, float]]: A tuple containing:
                - The preprocessed image (np.ndarray).
                - A tuple of two float values representing the padding applied (left/right, top/bottom).
        '''
        img_resized, pad = self.letterbox(img, new_shape=(
            self.input_shape[1], self.input_shape[2]))
        img_resized = img_resized.astype(np.float32) / 255.0
        # TFLite expects NHWC
        img_resized = np.expand_dims(
            img_resized, axis=0).astype(self.input_dtype)
        return img_resized, pad

    def postprocess(self, img: np.ndarray, outputs: np.ndarray,
                    pad: Tuple[float, float]) -> np.ndarray:
        '''
        Performs post-processing on the model's output to extract bounding boxes, scores, and class IDs.
        Args:
            img (numpy.ndarray): The input image.
            outputs (numpy.ndarray): The output of the model.
            pad (Tuple[float, float]): Padding used by letterbox.
        Returns:
            numpy.ndarray: The input image with detections drawn on it.
        '''
        # outputs shape: [1, N, 85] where 85 = 4
