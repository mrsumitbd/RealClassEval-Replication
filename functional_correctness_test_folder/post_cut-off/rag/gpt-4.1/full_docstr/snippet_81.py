import numpy as np
import cv2
from typing import Tuple, Union, Optional
try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite


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

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):
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
        self.metadata = metadata
        self.interpreter = tflite.Interpreter(model_path=model)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_shape = self.input_details[0]['shape']
        self.input_height = self.input_shape[1]
        self.input_width = self.input_shape[2]
        self.class_names = None
        if metadata is not None:
            try:
                with open(metadata, 'r') as f:
                    self.class_names = [line.strip()
                                        for line in f if line.strip()]
            except Exception:
                self.class_names = None

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        '''Resizes and reshapes images while maintaining aspect ratio by adding padding, suitable for YOLO models.'''
        shape = img.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
        dw = new_shape[1] - new_unpad[0]
        dh = new_shape[0] - new_unpad[1]
        dw /= 2  # divide padding into 2 sides
        dh /= 2

        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
        return img, (r, dw, dh)

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:
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
        x1, y1, w, h = box.astype(int)
        x2, y2 = x1 + w, y1 + h
        color = (0, 255, 0)
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label = f"{self.class_names[class_id] if self.class_names and class_id < len(self.class_names) else class_id}: {score:.2f}"
        (tw, th), baseline = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - th - baseline), (x1 + tw, y1), color, -1)
        cv2.putText(img, label, (x1, y1 - baseline),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float, float]]:
        '''
        Preprocesses the input image before performing inference.
        Args:
            img (np.ndarray): The input image to be preprocessed.
        Returns:
            Tuple[np.ndarray, Tuple[float, float, float]]: A tuple containing:
                - The preprocessed image (np.ndarray).
                - A tuple of (resize ratio, pad_w, pad_h).
        '''
        img0 = img.copy()
        img, (r, dw, dh) = self.letterbox(
            img0, (self.input_height, self.input_width))
        img = img.astype(np.float32)
        img /= 255.0
        if len(img.shape) == 3:
            img = np.expand_dims(img, axis=0)
        img = np.transpose(
            img, (0, 3, 1, 2)) if self.input_details[0]['shape'][1] == 3 else img
        return img, (r, dw, dh)

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float, float]) -> np.ndarray:
        '''
        Performs post-processing on the model's output to extract bounding boxes, scores, and class IDs.
        Args:
            img (numpy.ndarray): The input image.
            outputs (numpy.ndarray): The output of the model.
            pad (Tuple[float, float, float]): (resize ratio, pad_w, pad_h) used by letterbox.
        Returns:
            numpy.ndarray: The input image with detections drawn on it.
        '''
        r, dw, dh = pad
        h0, w0 = img.shape[:2]
        detections = outputs[0] if outputs.ndim == 3 else outputs
        boxes = []
        scores = []
        class_ids = []
        for det in detections:
            if det[4] < self.conf:
                continue
            class_id = int(np.argmax(det[5:]))
            score = det[4] * det[5 + class_id]
            if score < self.conf:
                continue
            x, y, w, h = det[0], det[1], det[2], det[3]
            # Undo letterbox
            x1 = (x - w / 2 - dw) / r
            y1 = (y - h / 2 - dh) / r
            w_box = w / r
            h_box = h / r
            boxes.append([x1, y1, w_box, h_box])
            scores.append(score)
            class_ids.append(class_id)
        if not boxes:
            return img
        boxes = np.array(boxes)
        scores = np.array(scores)
        class_ids = np.array(class_ids)
        # NMS
        indices = cv2.dnn.NMSBoxes(
            bboxes=boxes.tolist(),
            scores=scores.tolist(),
            score_threshold=self.conf,
            nms_threshold=self.iou
        )
        if len(indices) == 0:
            return img
        for i in indices.flatten():
            self.draw_detections(img, boxes[i], scores[i], class_ids[i])
        return img

    def detect(self, img_path: str) -> np.ndarray:
        '''
        Performs inference using a TFLite model and returns the output image with drawn detections.
        Args:
            img_path (str): The path to the input image file.
        Returns:
            np.ndarray: The output image with drawn detections.
        '''
        img0 = cv2.imread(img_path)
        if img0 is None:
            raise FileNotFoundError(f"Image not found: {img_path}")
        img, pad = self.preprocess(img0)
        input_data = img.astype(self.input_details[0]['dtype'])
        if self.input_details[0]['shape'][1] == 3:
            input_data = np.transpose(input_data, (0, 2, 3, 1))
        self.interpreter.set_tensor(self.input_details[0]['index'], input_data)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(
            self.output_details[0]['index'])
        result_img = self.postprocess(img0, output_data, pad)
        return result_img
