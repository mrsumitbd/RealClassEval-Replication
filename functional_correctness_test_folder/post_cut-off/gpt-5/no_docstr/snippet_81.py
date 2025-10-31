import cv2
import numpy as np
from typing import Tuple, Union, List, Optional
import random

try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow as tf
    tflite = tf.lite


class YOLOv8TFLite:

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):
        self.interpreter = tflite.Interpreter(model_path=model)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        inp = self.input_details[0]
        self.input_index = inp["index"]
        self.input_shape = tuple(inp["shape"])
        # Expect [1, h, w, 3]
        self.input_h = int(self.input_shape[1])
        self.input_w = int(self.input_shape[2])
        self.input_dtype = inp["dtype"]
        self.is_quant = self.input_dtype == np.uint8

        # Quantization parameters if present
        self.input_scale = inp.get(
            "quantization_parameters", {}).get("scales", None)
        self.input_zero_point = inp.get(
            "quantization_parameters", {}).get("zero_points", None)
        if isinstance(self.input_scale, np.ndarray) and self.input_scale.size > 0:
            self.input_scale = float(self.input_scale[0])
        else:
            self.input_scale = None
        if isinstance(self.input_zero_point, np.ndarray) and self.input_zero_point.size > 0:
            self.input_zero_point = int(self.input_zero_point[0])
        else:
            self.input_zero_point = None

        # Load class names if provided
        self.class_names: List[str] = []
        if metadata:
            try:
                with open(metadata, "r", encoding="utf-8") as f:
                    self.class_names = [line.strip()
                                        for line in f if line.strip()]
            except Exception:
                self.class_names = []
        self.num_classes = len(self.class_names) if self.class_names else 80

        # Colors for classes
        random.seed(0)
        self.colors = [tuple(int(c) for c in np.random.randint(0, 255, 3))
                       for _ in range(max(self.num_classes, 80))]

        self.conf = float(conf)
        self.iou = float(iou)

        # to keep last image shape for scaling back
        self.last_orig_shape: Tuple[int, int] = (0, 0)

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        h0, w0 = img.shape[:2]
        new_h, new_w = int(new_shape[0]), int(new_shape[1])
        scale = min(new_w / w0, new_h / h0)
        nw, nh = int(round(w0 * scale)), int(round(h0 * scale))
        resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)

        canvas = np.full((new_h, new_w, 3), 114, dtype=img.dtype)
        dw = (new_w - nw) // 2
        dh = (new_h - nh) // 2
        canvas[dh:dh + nh, dw:dw + nw] = resized
        return canvas, (float(dw), float(dh))

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:
        x1, y1, x2, y2 = [int(v) for v in box]
        color = self.colors[int(class_id) % len(self.colors)]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label = f"{class_id}:{score:.2f}"
        if self.class_names and 0 <= int(class_id) < len(self.class_names):
            label = f"{self.class_names[int(class_id)]}:{score:.2f}"
        (tw, th), bl = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 4, y1), color, -1)
        cv2.putText(img, label, (x1 + 2, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        self.last_orig_shape = (img.shape[0], img.shape[1])  # (h, w)
        lb_img, pad = self.letterbox(img, (self.input_h, self.input_w))
        rgb = cv2.cvtColor(lb_img, cv2.COLOR_BGR2RGB)

        if self.is_quant:
            inp = rgb.astype(np.uint8)
            if self.input_scale is not None and self.input_zero_point is not None:
                # Assume model expects quantized input; values directly as uint8 typically ok.
                pass
        else:
            inp = rgb.astype(np.float32) / 255.0

        inp = np.expand_dims(inp, axis=0)
        return inp, pad

    def _xywh_to_xyxy(self, boxes: np.ndarray) -> np.ndarray:
        x, y, w, h = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
        x1 = x - w / 2
        y1 = y - h / 2
        x2 = x + w / 2
        y2 = y + h / 2
        return np.stack([x1, y1, x2, y2], axis=-1)

    def _nms(self, boxes: np.ndarray, scores: np.ndarray, iou_thr: float) -> List[int]:
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]
        areas = (x2 - x1).clip(min=0) * (y2 - y1).clip(min=0)
        order = scores.argsort()[::-1]
        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            w = (xx2 - xx1).clip(min=0)
            h = (yy2 - yy1).clip(min=0)
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter + 1e-9)
            inds = np.where(ovr <= iou_thr)[0]
            order = order[inds + 1]
        return keep

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        oh, ow = self.last_orig_shape
        ih, iw = self.input_h, self.input_w
        dw, dh = pad
        scale = min(iw / ow, ih / oh)

        if outputs.ndim == 3 and outputs.shape[0] == 1:
            preds = outputs[0]
        elif outputs.ndim == 2:
            preds = outputs
        else:
            preds = outputs.reshape((-1, outputs.shape[-1]))

        # Ensure shape (N, C)
        if preds.shape[0] <= preds.shape[1] and preds.shape[1] in (84, 85):
            pass
        elif preds.shape[1] <= preds.shape[0] and preds.shape[0] in (84, 85):
            preds = preds.T
        elif preds.shape[-1] < preds.shape[0]:
            preds = preds.T

        nC = preds.shape[1]
        if nC not in (84, 85):
            # Fallback: assume 4 + num_classes
            pass

        # YOLOv8 TFLite usually: 4 box + num_classes (no obj)
        boxes_xywh = preds[:, :4]
        cls_scores = preds[:, 4:]  # (N, num_classes possibly 80 or 81)

        # If there is an objectness score (85 with 1 obj + 80 classes), combine
        if nC == 85 and cls_scores.shape[1] >= 81:
            obj = cls_scores[:, 0:1]
            cls_scores = cls_scores[:, 1:] * obj

        # Take best class per detection
        class_ids = np.argmax(cls_scores, axis=1)
        confidences = cls_scores[np.arange(cls_scores.shape[0]), class_ids]

        # Threshold by confidence
        mask = confidences >= self.conf
        if not np.any(mask):
            return np.zeros((0, 6), dtype=np.float32)

        boxes_xywh = boxes_xywh[mask]
        confidences = confidences[mask]
        class_ids = class_ids[mask].astype(np.int32)

        # Boxes are in resized+letterboxed image coordinates
        boxes_xyxy = self._xywh_to_xyxy(boxes_xywh)
        # Undo padding
        boxes_xyxy[:, [0, 2]] -= dw
        boxes_xyxy[:, [1, 3]] -= dh
        # Undo scale to original image size
        boxes_xyxy /= scale

        # Clip to image bounds
        boxes_xyxy[:, [0, 2]] = boxes_xyxy[:, [0, 2]].clip(0, ow - 1)
        boxes_xyxy[:, [1, 3]] = boxes_xyxy[:, [1, 3]].clip(0, oh - 1)

        # NMS per class
        final_boxes = []
        final_scores = []
        final_classes = []
        for c in np.unique(class_ids):
            idxs = np.where(class_ids == c)[0]
            keep = self._nms(boxes_xyxy[idxs], confidences[idxs], self.iou)
            if keep:
                final_boxes.append(boxes_xyxy[idxs][keep])
                final_scores.append(confidences[idxs][keep])
                final_classes.append(np.full(len(keep), c, dtype=np.int32))
        if len(final_boxes) == 0:
            return np.zeros((0, 6), dtype=np.float32)

        final_boxes = np.concatenate(final_boxes, axis=0)
        final_scores = np.concatenate(final_scores, axis=0)
        final_classes = np.concatenate(final_classes, axis=0)

        dets = np.concatenate(
            [final_boxes.astype(np.float32),
             final_scores.reshape(-1, 1).astype(np.float32),
             final_classes.reshape(-1, 1).astype(np.float32)],
            axis=1
        )
        return dets

    def detect(self, img_path: str) -> np.ndarray:
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"Could not read image at path: {img_path}")

        inp, pad = self.preprocess(img)

        # Set input tensor
        if self.is_quant and self.input_scale and self.input_zero_point is not None and inp.dtype != np.uint8:
            q = (inp / self.input_scale +
                 self.input_zero_point).round().astype(np.uint8)
            self.interpreter.set_tensor(self.input_index, q)
        else:
            self.interpreter.set_tensor(self.input_index, inp)

        self.interpreter.invoke()

        # Get first output (Ultralytics tflite models have single output)
        out_detail = self.output_details[0]
        out = self.interpreter.get_tensor(out_detail["index"])

        # Dequantize if needed
        out_scale = out_detail.get(
            "quantization_parameters", {}).get("scales", None)
        out_zero = out_detail.get(
            "quantization_parameters", {}).get("zero_points", None)
        if isinstance(out_scale, np.ndarray) and out_scale.size > 0 and out.dtype == np.uint8:
            s = float(out_scale[0])
            z = int(out_zero[0]) if isinstance(
                out_zero, np.ndarray) and out_zero.size > 0 else 0
            outputs = (out.astype(np.float32) - z) * s
        else:
            outputs = out.astype(np.float32)

        dets = self.postprocess(img, outputs, pad)

        # Draw detections
        for det in dets:
            box = det[:4]
            score = float(det[4])
            cls_id = int(det[5])
            self.draw_detections(img, box, score, cls_id)

        return img
