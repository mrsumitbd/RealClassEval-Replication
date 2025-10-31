import os
import json
from typing import Tuple, Union, Optional, List

import numpy as np
import cv2


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
        self.conf = float(conf)
        self.iou = float(iou)
        self.metadata_path = metadata
        self.names: Optional[List[str]] = None

        # Load class names from metadata if available
        if self.metadata_path and os.path.isfile(self.metadata_path):
            self.names = self._load_class_names(self.metadata_path)

        # Initialize TFLite interpreter
        self.interpreter = self._create_interpreter(self.model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Input specs
        in_shape = self.input_details[0]['shape']
        # handle dynamic shapes (some TFLite models use -1)
        self.input_height = int(in_shape[1] if in_shape[1] > 0 else 640)
        self.input_width = int(in_shape[2] if in_shape[2] > 0 else 640)
        self.input_dtype = self.input_details[0]['dtype']
        self.input_quant = self.input_details[0].get(
            'quantization_parameters', None)
        if self.input_quant and 'scales' in self.input_quant and len(self.input_quant['scales']) > 0:
            self.input_scale = float(self.input_quant['scales'][0])
            self.input_zero_point = int(self.input_quant['zero_points'][0])
        else:
            # Fallback for classic quantization tuple
            q = self.input_details[0].get('quantization', (0.0, 0))
            self.input_scale = float(q[0])
            self.input_zero_point = int(q[1] if len(q) > 1 else 0)

        # Will be set per image
        self._scale: float = 1.0
        self._pad: Tuple[float, float] = (0.0, 0.0)  # (pad_y, pad_x)

        # Colors for classes
        self._colors = [tuple(int(c) for c in np.random.RandomState(
            i).randint(0, 255, 3)) for i in range(1000)]

    def _create_interpreter(self, model_path: str):
        try:
            from tflite_runtime.interpreter import Interpreter
            return Interpreter(model_path=model_path)
        except Exception:
            try:
                import tensorflow as tf
                return tf.lite.Interpreter(model_path=model_path)
            except Exception as e:
                raise RuntimeError(f'Failed to load TFLite interpreter: {e}')

    def _load_class_names(self, path: str) -> Optional[List[str]]:
        ext = os.path.splitext(path)[1].lower()
        try:
            if ext in ('.json',):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, dict) and 'names' in data:
                    names = data['names']
                    if isinstance(names, dict):
                        # sort by key
                        return [names[k] for k in sorted(names.keys(), key=lambda x: int(x) if str(x).isdigit() else str(x))]
                    if isinstance(names, list):
                        return [str(x) for x in names]
                if isinstance(data, list):
                    return [str(x) for x in data]
            elif ext in ('.yml', '.yaml'):
                try:
                    import yaml
                    with open(path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f)
                    if isinstance(data, dict) and 'names' in data:
                        names = data['names']
                        if isinstance(names, dict):
                            return [names[k] for k in sorted(names.keys(), key=lambda x: int(x) if str(x).isdigit() else str(x))]
                        if isinstance(names, list):
                            return [str(x) for x in names]
                except Exception:
                    return None
            else:
                # Treat as txt with one name per line
                with open(path, 'r', encoding='utf-8') as f:
                    lines = [line.strip() for line in f if line.strip()]
                if lines:
                    return lines
        except Exception:
            return None
        return None

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        '''Resizes and reshapes images while maintaining aspect ratio by adding padding, suitable for YOLO models.'''
        h0, w0 = img.shape[:2]
        new_h, new_w = int(new_shape[0]), int(new_shape[1])

        r = min(new_w / w0, new_h / h0)
        w = int(round(w0 * r))
        h = int(round(h0 * r))

        dw = new_w - w
        dh = new_h - h
        dw_half, dh_half = int(round(dw / 2)), int(round(dh / 2))

        if (w0, h0) != (w, h):
            img = cv2.resize(img, (w, h), interpolation=cv2.INTER_LINEAR)

        top, bottom = dh_half, dh - dh_half
        left, right = dw_half, dw - dw_half
        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))

        self._scale = r
        # store pad in (pad_y, pad_x)
        self._pad = (float(dh_half), float(dw_half))
        return img, (float(dh_half), float(dw_half))

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
        x, y, w, h = float(box[0]), float(box[1]), float(box[2]), float(box[3])
        x1, y1 = int(round(x)), int(round(y))
        x2, y2 = int(round(x + w)), int(round(y + h))
        color = self._colors[int(class_id) % len(self._colors)]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        if self.names and 0 <= int(class_id) < len(self.names):
            label_text = f'{self.names[int(class_id)]} {float(score):.2f}'
        else:
            label_text = f'{int(class_id)} {float(score):.2f}'
        (tw, th), baseline = cv2.getTextSize(
            label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - th - baseline), (x1 + tw, y1), color, -1)
        cv2.putText(img, label_text, (x1, y1 - baseline),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        '''
        Preprocesses the input image before performing inference.
        Args:
            img (np.ndarray): The input image to be preprocessed.
        Returns:
            Tuple[np.ndarray, Tuple[float, float]]: A tuple containing:
                - The preprocessed image (np.ndarray).
                - A tuple of two float values representing the padding applied (top/bottom, left/right).
        '''
        # Convert BGR to RGB
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        padded, pad = self.letterbox(
            rgb, (self.input_height, self.input_width))
        input_tensor = padded.astype(np.float32)

        if self.input_dtype == np.uint8 and self.input_scale > 0:
            # quantized input
            input_tensor = np.clip(input_tensor / 1.0, 0, 255).astype(np.uint8)
            if self.input_zero_point != 0 or abs(self.input_scale - 1.0) > 1e-6:
                # If scale not 1, apply quantization
                input_tensor = (input_tensor / (255.0 / (1.0 / self.input_scale)
                                                ) + self.input_zero_point).astype(np.uint8)
        else:
            input_tensor = input_tensor / 255.0

        input_tensor = np.expand_dims(input_tensor, axis=0)  # (1, H, W, 3)
        return input_tensor, pad

    def _nms(self, boxes_xyxy: np.ndarray, scores: np.ndarray, iou_thres: float) -> List[int]:
        x1 = boxes_xyxy[:, 0]
        y1 = boxes_xyxy[:, 1]
        x2 = boxes_xyxy[:, 2]
        y2 = boxes_xyxy[:, 3]

        areas = (x2 - x1 + 1e-5) * (y2 - y1 + 1e-5)
        order = scores.argsort()[::-1]
        keep = []
        while order.size > 0:
            i = int(order[0])
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            w = np.maximum(0.0, xx2 - xx1)
            h = np.maximum(0.0, yy2 - yy1)
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter + 1e-5)
            inds = np.where(ovr <= iou_thres)[0]
            order = order[inds + 1]
        return keep

    def _scale_coords_to_original(self, boxes_xyxy: np.ndarray, img_shape: Tuple[int, int]) -> np.ndarray:
        # boxes are in input (letterboxed) coordinates, convert back to original image size
        h0, w0 = img_shape
        pad_y, pad_x = self._pad
        r = self._scale
        # subtract padding and scale back
        boxes = boxes_xyxy.copy()
        boxes[:, [0, 2]] = (boxes[:, [0, 2]] - pad_x) / r
        boxes[:, [1, 3]] = (boxes[:, [1, 3]] - pad_y) / r
        # clip
        boxes[:, 0] = np.clip(boxes[:, 0], 0, w0 - 1)
        boxes[:, 2] = np.clip(boxes[:, 2], 0, w0 - 1)
        boxes[:, 1] = np.clip(boxes[:, 1], 0, h0 - 1)
        boxes[:, 3] = np.clip(boxes[:, 3], 0, h0 - 1)
        return boxes

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        '''
        Performs post-processing on the model's output to extract bounding boxes, scores, and class IDs.
        Args:
            img (numpy.ndarray): The input image.
            outputs (numpy.ndarray): The output of the model.
            pad (Tuple[float, float]): Padding used by letterbox.
        Returns:
            numpy.ndarray: The input image with detections drawn on it.
        '''
        h0, w0 = img.shape[:2]
        boxes_xyxy = []
        scores = []
        classes = []

        # Normalize outputs format
        outs = outputs
        if isinstance(outs, np.ndarray):
            outs = [outs]
        elif isinstance(outs, tuple):
            outs = list(outs)

        # Try to detect common TFLite NMS output signature
        boxes_arr = None
        scores_arr = None
        classes_arr = None
        for arr in outs:
            shape = arr.shape
            if len(shape) == 3 and shape[-1] == 4:
                boxes_arr = arr
            elif len(shape) == 2 and shape[-1] == 4 and shape[0] == 1:
                boxes_arr = arr.reshape(1, -1, 4)
            elif len(shape) == 2 and shape[0] == 1:
                # could be scores or classes
                if arr.dtype.kind in ('f',):
                    scores_arr = arr
                else:
                    classes_arr = arr
            elif len(shape) == 3 and shape[-1] == 1:
                # num_detections or classes as float
                pass

        parsed = False
        if boxes_arr is not None and (scores_arr is not None) and (classes_arr is not None):
            # Assume TF NMS format: boxes: (1, N, 4) as [ymin, xmin, ymax, xmax] normalized
            b = boxes_arr[0]
            s = scores_arr[0]
            c = classes_arr[0].astype(int)

            # Remove low-confidence
            keep = s >= self.conf
            b = b[keep]
            s = s[keep]
            c = c[keep]
            if b.size > 0:
                # If values look normalized
                if np.max(b) <= 1.5:
                    b[:, [0, 2]] *= self.input_height
                    b[:, [1, 3]] *= self.input_width
                # Convert to xyxy in letterboxed space
                xyxy = np.stack([b[:, 1], b[:, 0], b[:, 3], b[:, 2]], axis=1)
                boxes_xyxy = xyxy
                scores = s
                classes = c
                parsed = True

        if not parsed:
            # Try Ultralytics-like output: (1, N, 6) -> [x1,y1,x2,y2,score,cls]
            for arr in outs:
                a = arr
                if a.ndim == 3 and a.shape[0] == 1 and a.shape[-1] == 6:
                    preds = a[0]
                    s = preds[:, 4]
                    c = preds[:, 5].astype(int)
                    keep = s >= self.conf
                    preds = preds[keep]
                    if preds.size > 0:
                        boxes_xyxy = preds[:, :4]
                        scores = preds[:, 4]
                        classes = preds[:, 5].astype(int)
                        parsed = True
                        break

        if not parsed:
            # Raw YOLOv8 head output (no NMS): shapes like (1, 84, 8400) or (1, 8400, 84)
            for arr in outs:
                a = arr
                if a.ndim == 3 and a.shape[0] == 1 and (a.shape[1] == 84 or a.shape[2] == 84):
                    if a.shape[1] == 84:
                        pred = np.transpose(a[0], (1, 0))  # (N, 84)
                    else:
                        pred = a[0]  # (N, 84)
                    boxes_xywh = pred[:, :4]
                    cls_scores = pred[:, 4:]
                    class_ids = np.argmax(cls_scores, axis=1)
                    confs = cls_scores[np.arange(
                        cls_scores.shape[0]), class_ids]
                    keep = confs >= self.conf
                    boxes_xywh = boxes_xywh[keep]
                    confs = confs[keep]
                    class_ids = class_ids[keep]

                    if boxes_xywh.size > 0:
                        # Convert xywh -> xyxy
                        xyxy = np.zeros_like(boxes_xywh)
                        xyxy[:, 0] = boxes_xywh[:, 0] - boxes_xywh[:, 2] / 2.0
                        xyxy[:, 1] = boxes_xywh[:, 1] - boxes_xywh[:, 3] / 2.0
                        xyxy[:, 2] = boxes_xywh[:, 0] + boxes_xywh[:, 2] / 2.0
                        xyxy[:, 3] = boxes_xywh[:, 1] + boxes_xywh[:, 3] / 2.0

                        # NMS
                        keep_inds = self._nms(xyxy, confs, self.iou)
                        boxes_xyxy = xyxy[keep_inds]
                        scores = confs[keep_inds]
                        classes = class_ids[keep_inds]
                        parsed = True
                        break

        # If parsed and we have detections, map to original image coordinates and draw
        if isinstance(boxes_xyxy, list):
            boxes_xyxy = np.array(boxes_xyxy)
        if isinstance(scores, list):
            scores = np.array(scores)
        if isinstance(classes, list):
            classes = np.array(classes, dtype=int)

        if boxes_xyxy is None or len(np.shape(boxes_xyxy)) == 0 or boxes_xyxy.size == 0:
            return img

        boxes_xyxy = boxes_xyxy.astype(np.float32)
        boxes_xyxy = self._scale_coords_to_original(boxes_xyxy, (h0, w0))

        # Convert to xywh for drawing
        boxes_xywh = np.zeros_like(boxes_xyxy)
        boxes_xywh[:, 0] = boxes_xyxy[:, 0]
        boxes_xywh[:, 1] = boxes_xyxy[:, 1]
        boxes_xywh[:, 2] = boxes_xyxy[:, 2] - boxes_xyxy[:, 0]
        boxes_xywh[:, 3] = boxes_xyxy[:, 3] - boxes_xyxy[:, 1]

        for i in range(boxes_xywh.shape[0]):
            self.draw_detections(img, boxes_xywh[i], float(
                scores[i]), int(classes[i]))
        return img

    def detect(self, img_path: str) -> np.ndarray:
        '''
        Performs inference using a TFLite model and returns the output image with drawn detections.
        Args:
            img_path (str): The path to the input image file.
        Returns:
            np.ndarray: The output image with drawn detections.
        '''
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f'Image not found: {img_path}')

        input_tensor, pad = self.preprocess(img)

        # Handle dynamic shapes
        in_idx = self.input_details[0]['index']
        in_shape = self.input_details[0]['shape']
        desired_shape = (1, self.input_height, self.input_width, 3)
        if tuple(in_shape) != desired_shape:
            try:
                self.interpreter.resize_tensor_input(in_idx, desired_shape)
                self.interpreter.allocate_tensors()
                self.input_details = self.interpreter.get_input_details()
                self.output_details = self.interpreter.get_output_details()
            except Exception:
                pass

        # Set input tensor
        self.interpreter.set_tensor(
            self.input_details[0]['index'], input_tensor)
        self.interpreter.invoke()

        # Gather outputs
        outs = []
        for od in self.output_details:
            out = self.interpreter.get_tensor(od['index'])
            outs.append(out)

        # Postprocess and draw
        result_img = self.postprocess(img.copy(), outs, pad)
        return result_img
