import os
from typing import Tuple, Union, Optional, List
import numpy as np
import cv2

try:
    from tflite_runtime.interpreter import Interpreter
except Exception:
    from tensorflow.lite import Interpreter


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

        if not os.path.isfile(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")

        self.interpreter = Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()

        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Assume single input
        in_shape = self.input_details[0]["shape"]
        # Handle both [1, H, W, C] and dynamic shapes
        if len(in_shape) == 4:
            self.in_h = int(in_shape[1])
            self.in_w = int(in_shape[2])
        else:
            # Fallback to default YOLO size
            self.in_h = 640
            self.in_w = 640

        # Set expected dtype
        self.input_dtype = self.input_details[0]["dtype"]

        # Labels
        self.class_names = self._load_labels(self.metadata_path)

        # Color palette for drawing
        self.colors = self._generate_colors(300)

        # State from last preprocess
        self._last_ratio = 1.0
        self._last_pad = (0.0, 0.0)
        self._last_shape = (self.in_h, self.in_w)

    def _load_labels(self, path: Optional[str]) -> List[str]:
        if path is None:
            # Default COCO 80 placeholder
            return [str(i) for i in range(80)]
        if not os.path.isfile(path):
            return [str(i) for i in range(80)]
        with open(path, "r", encoding="utf-8") as f:
            labels = [ln.strip() for ln in f if ln.strip()]
        return labels if labels else [str(i) for i in range(80)]

    def _generate_colors(self, n: int) -> List[Tuple[int, int, int]]:
        rng = np.random.default_rng(12345)
        colors = (rng.integers(0, 255, size=(n, 3))).tolist()
        return [tuple(map(int, c)) for c in colors]

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        '''Resizes and reshapes images while maintaining aspect ratio by adding padding, suitable for YOLO models.'''
        shape = img.shape[:2]  # (h, w)
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)
        new_h, new_w = int(new_shape[0]), int(new_shape[1])

        r = min(new_h / shape[0], new_w / shape[1])
        new_unpad = (int(round(shape[1] * r)), int(round(shape[0] * r)))
        dw, dh = new_w - new_unpad[0], new_h - new_unpad[1]
        dw /= 2
        dh /= 2

        if shape[::-1] != new_unpad:
            img_resized = cv2.resize(
                img, new_unpad, interpolation=cv2.INTER_LINEAR)
        else:
            img_resized = img.copy()

        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img_padded = cv2.copyMakeBorder(
            img_resized, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))

        return img_padded, (dh, dw)

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
        color = self.colors[int(class_id) % len(self.colors)]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)

        cls_name = str(class_id)
        if 0 <= int(class_id) < len(self.class_names):
            cls_name = self.class_names[int(class_id)]

        label = f"{cls_name} {float(score):.2f}"
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        th = th + 6
        cv2.rectangle(img, (x1, y1 - th if y1 - th > 0 else y1),
                      (x1 + tw, y1), color, -1)
        cv2.putText(img, label, (x1, y1 - 3 if y1 - 3 > 0 else y1 + th - 3),
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
        self._last_shape = img.shape[:2]
        lb_img, pad = self.letterbox(img, (self.in_h, self.in_w))
        # Compute ratio used
        r = min(self.in_h / max(1,
                self._last_shape[0]), self.in_w / max(1, self._last_shape[1]))
        self._last_ratio = r
        self._last_pad = pad

        # Normalize to 0-1 and ensure dtype matches model
        inp = lb_img.astype(np.float32) / 255.0
        # HWC to match TFLite models (most YOLOv8 TFLite expect [1, H, W, 3])
        if self.input_dtype == np.uint8:
            inp = (inp * 255.0).round().astype(np.uint8)
        inp = np.expand_dims(inp, 0)  # [1, H, W, 3]
        return inp, pad

    def _xywh_to_xyxy(self, boxes: np.ndarray) -> np.ndarray:
        x, y, w, h = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
        x1 = x - w / 2
        y1 = y - h / 2
        x2 = x + w / 2
        y2 = y + h / 2
        return np.stack([x1, y1, x2, y2], axis=1)

    def _nms(self, boxes: np.ndarray, scores: np.ndarray, iou_thres: float) -> List[int]:
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        areas = (x2 - x1).clip(min=0) * (y2 - y1).clip(min=0)
        order = scores.argsort()[::-1]

        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(int(i))

            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            w = (xx2 - xx1).clip(min=0)
            h = (yy2 - yy1).clip(min=0)
            inter = w * h
            union = areas[i] + areas[order[1:]] - inter + 1e-6
            iou = inter / union

            inds = np.where(iou <= iou_thres)[0]
            order = order[inds + 1]
        return keep

    def _scale_boxes_back(self, boxes_xyxy: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        dh, dw = pad
        # Remove padding
        boxes = boxes_xyxy.copy()
        boxes[:, [0, 2]] -= dw
        boxes[:, [1, 3]] -= dh
        # Scale back using inverse ratio
        r = self._last_ratio if self._last_ratio != 0 else 1.0
        boxes /= r
        # Clip to image size
        h0, w0 = self._last_shape
        boxes[:, 0] = np.clip(boxes[:, 0], 0, w0 - 1)
        boxes[:, 2] = np.clip(boxes[:, 2], 0, w0 - 1)
        boxes[:, 1] = np.clip(boxes[:, 1], 0, h0 - 1)
        boxes[:, 3] = np.clip(boxes[:, 3], 0, h0 - 1)
        return boxes

    def _parse_outputs(self, raw: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        # Returns (boxes_xyxy_in_model_space, scores, class_ids)
        out = raw
        if isinstance(out, (list, tuple)):
            # If multiple outputs, try to find the largest
            shapes = [np.prod(o.shape) for o in out]
            out = out[int(np.argmax(shapes))]

        out = np.array(out)
        if out.ndim == 4:
            out = np.squeeze(out, axis=0)
        if out.ndim == 3:
            # Expect [1, C, N] or [1, N, C] squeezed to [C, N] or [N, C]
            if out.shape[0] in (84, 85) and out.shape[1] > out.shape[0]:
                out = out.transpose(1, 0)  # [N, C]
        elif out.ndim == 2:
            pass
        elif out.ndim == 1:
            # Unsupported
            out = out.reshape((-1, out.shape[-1]))

        N, C = out.shape[0], out.shape[1]

        # Heuristics:
        # Case 1: C >= 6 and likely [cx, cy, w, h, obj?, num_classes...]
        if C >= 6:
            cxcywh = out[:, :4]
            # Determine if objectness exists
            # If C == 4 + 1 + num_classes
            # Guess num_classes
            num_classes_guess = C - 5
            has_obj = num_classes_guess >= 1
            if has_obj and num_classes_guess <= 400:
                obj = out[:, 4:5]
                cls_scores = out[:, 5:]
                cls_id = np.argmax(cls_scores, axis=1)
                cls_prob = cls_scores[np.arange(N), cls_id]
                scores = (obj[:, 0] * cls_prob).astype(np.float32)
            else:
                # No objectness, assume [cx, cy, w, h, cls_scores...]
                cls_scores = out[:, 4:]
                cls_id = np.argmax(cls_scores, axis=1)
                scores = cls_scores[np.arange(N), cls_id].astype(np.float32)

            boxes_xyxy = self._xywh_to_xyxy(cxcywh)
            return boxes_xyxy, scores, cls_id.astype(int)

        # Case 2: Possibly [x1, y1, x2, y2, score, class]
        if C == 6:
            boxes_xyxy = out[:, :4]
            scores = out[:, 4].astype(np.float32)
            cls_id = np.rint(out[:, 5]).astype(int)
            return boxes_xyxy, scores, cls_id

        # Fallback: try to interpret as [N, 6] with xyxy
        if C > 6:
            boxes_xyxy = out[:, :4]
            cls_scores = out[:, 4:]
            cls_id = np.argmax(cls_scores, axis=1)
            scores = cls_scores[np.arange(N), cls_id].astype(np.float32)
            return boxes_xyxy, scores, cls_id.astype(int)

        # If none matched, return empty
        return np.zeros((0, 4), dtype=np.float32), np.zeros((0,), dtype=np.float32), np.zeros((0,), dtype=int)

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
        boxes_xyxy_model, scores, class_ids = self._parse_outputs(outputs)
        if boxes_xyxy_model.size == 0:
            return img

        # Filter by confidence
        keep = scores >= float(self.conf)
        boxes_xyxy_model = boxes_xyxy_model[keep]
        scores = scores[keep]
        class_ids = class_ids[keep]

        if boxes_xyxy_model.size == 0:
            return img

        # Scale boxes back to original image
        boxes_xyxy = self._scale_boxes_back(boxes_xyxy_model, pad)

        # Per-class NMS
        final_indices = []
        for c in np.unique(class_ids):
            idxs = np.where(class_ids == c)[0]
            keep_idx = self._nms(boxes_xyxy[idxs], scores[idxs], self.iou)
            final_indices.extend(idxs[ki] for ki in keep_idx)

        if len(final_indices) == 0:
            return img

        final_indices = np.array(final_indices, dtype=int)
        boxes_xyxy = boxes_xyxy[final_indices]
        scores = scores[final_indices]
        class_ids = class_ids[final_indices]

        # Draw
        for b, s, cid in zip(boxes_xyxy, scores, class_ids):
            x1, y1, x2, y2 = b
            w = max(0, x2 - x1)
            h = max(0, y2 - y1)
            self.draw_detections(img, np.array([x1, y1, w, h]), s, int(cid))

        return img

    def detect(self, img_path: str) -> np.ndarray:
        '''
        Performs inference using a TFLite model and returns the output image with drawn detections.
        Args:
            img_path (str): The path to the input image file.
        Returns:
            np.ndarray: The output image with drawn detections.
        '''
        if not os.path.isfile(img_path):
            raise FileNotFoundError(f"Image file not found: {img_path}")

        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Failed to read image: {img_path}")

        inp, pad = self.preprocess(img)

        # Set input tensor
        index = self.input_details[0]["index"]
        if inp.dtype != self.input_dtype:
            inp_to_set = inp.astype(self.input_dtype)
        else:
            inp_to_set = inp
        self.interpreter.set_tensor(index, inp_to_set)

        self.interpreter.invoke()

        outputs = []
        for od in self.output_details:
            outputs.append(self.interpreter.get_tensor(od["index"]))
        # Pass all outputs to parser; it will select appropriate one
        result_img = self.postprocess(img.copy(), outputs, pad)
        return result_img
