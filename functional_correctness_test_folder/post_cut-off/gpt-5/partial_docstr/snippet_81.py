import cv2
import numpy as np
from typing import Tuple, Union, List

try:
    from tflite_runtime.interpreter import Interpreter
except Exception:
    from tensorflow.lite import Interpreter  # type: ignore


class YOLOv8TFLite:

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):
        self.interpreter = Interpreter(model_path=model)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        ih, iw = self.input_details[0]["shape"][1], self.input_details[0]["shape"][2]
        self.input_size = (iw, ih)
        self.conf_thres = float(conf)
        self.iou_thres = float(iou)

        self.class_names: List[str] = []
        if metadata is not None:
            try:
                with open(metadata, "r", encoding="utf-8") as f:
                    self.class_names = [line.strip()
                                        for line in f if line.strip()]
            except Exception:
                self.class_names = []
        self.num_classes = len(self.class_names) if self.class_names else 0

        self._last_scale: float = 1.0
        self._last_pad: Tuple[float, float] = (0.0, 0.0)
        self._last_orig_shape: Tuple[int, int] = (0, 0)  # (h, w)

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        h0, w0 = img.shape[:2]
        new_w, new_h = int(new_shape[0]), int(new_shape[1])
        scale = min(new_w / w0, new_h / h0)
        nw, nh = int(round(w0 * scale)), int(round(h0 * scale))

        resized = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)

        pad_w = new_w - nw
        pad_h = new_h - nh
        pad_left = pad_w // 2
        pad_right = pad_w - pad_left
        pad_top = pad_h // 2
        pad_bottom = pad_h - pad_top

        padded = cv2.copyMakeBorder(
            resized, pad_top, pad_bottom, pad_left, pad_right, cv2.BORDER_CONSTANT, value=(114, 114, 114))

        self._last_scale = scale
        self._last_pad = (float(pad_top), float(pad_left))
        return padded, (float(pad_top), float(pad_left))

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:
        x1, y1, x2, y2 = box.astype(int).tolist()
        color = (int((37 * (class_id + 1)) % 255), int((17 *
                 (class_id + 1)) % 255), int((29 * (class_id + 1)) % 255))
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        label = f"{class_id}:{score:.2f}"
        if self.class_names and 0 <= class_id < len(self.class_names):
            label = f"{self.class_names[class_id]}:{score:.2f}"
        (tw, th), bs = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - th - 6), (x1 + tw + 2, y1), color, -1)
        cv2.putText(img, label, (x1 + 1, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        self._last_orig_shape = (img.shape[0], img.shape[1])
        lb_img, pad = self.letterbox(
            img, (self.input_size[0], self.input_size[1]))
        img_rgb = cv2.cvtColor(lb_img, cv2.COLOR_BGR2RGB)
        img_float = img_rgb.astype(np.float32) / 255.0
        if self.input_details[0]["dtype"] == np.uint8:
            img_pre = (img_float * 255.0).astype(np.uint8)
        else:
            img_pre = img_float
        img_pre = np.expand_dims(img_pre, axis=0)
        return img_pre, pad

    def _xywh_to_xyxy(self, xywh: np.ndarray) -> np.ndarray:
        x, y, w, h = xywh
        return np.array([x - w / 2, y - h / 2, x + w / 2, y + h / 2], dtype=np.float32)

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
            iou = inter / (areas[i] + areas[order[1:]] - inter + 1e-7)

            inds = np.where(iou <= iou_thres)[0]
            order = order[inds + 1]
        return keep

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        if isinstance(outputs, list):
            out = outputs[0]
        else:
            out = outputs
        out = np.squeeze(out)
        if out.ndim == 1:
            out = np.expand_dims(out, 0)

        detections: List[Tuple[np.ndarray, float, int]] = []
        for det in out:
            if det.size < 6:
                continue
            box = det[:4]
            rest = det[4:]
            if rest.size == 1:
                score = float(rest[0])
                class_id = 0
            elif rest.size == 2:
                score = float(rest[0])
                class_id = int(rest[1])
            else:
                # Handle 4 + C   or 4 + 1 + C
                if rest.size >= 2 and (self.num_classes == 0 or rest.size - 1 != self.num_classes):
                    # attempt to detect if there's an objectness
                    # assume format: obj + C
                    obj = rest[0]
                    cls_scores = rest[1:]
                    cls_id = int(np.argmax(cls_scores))
                    cls_prob = float(cls_scores[cls_id])
                    score = float(obj) * cls_prob
                    class_id = cls_id
                else:
                    cls_scores = rest
                    cls_id = int(np.argmax(cls_scores))
                    score = float(cls_scores[cls_id])
                    class_id = cls_id

            if score < self.conf_thres:
                continue

            xyxy = self._xywh_to_xyxy(box.astype(np.float32))
            pad_y, pad_x = pad
            scale = self._last_scale
            # remove padding and scale back to original size
            x1 = (xyxy[0] - pad_x) / max(scale, 1e-9)
            y1 = (xyxy[1] - pad_y) / max(scale, 1e-9)
            x2 = (xyxy[2] - pad_x) / max(scale, 1e-9)
            y2 = (xyxy[3] - pad_y) / max(scale, 1e-9)

            h0, w0 = self._last_orig_shape
            x1 = float(np.clip(x1, 0, w0 - 1))
            y1 = float(np.clip(y1, 0, h0 - 1))
            x2 = float(np.clip(x2, 0, w0 - 1))
            y2 = float(np.clip(y2, 0, h0 - 1))

            if x2 <= x1 or y2 <= y1:
                continue

            detections.append(
                (np.array([x1, y1, x2, y2], dtype=np.float32), score, class_id))

        if not detections:
            return img

        boxes = np.stack([d[0] for d in detections], axis=0)
        scores = np.array([d[1] for d in detections], dtype=np.float32)
        class_ids = np.array([d[2] for d in detections], dtype=int)

        final_indices: List[int] = []
        for c in np.unique(class_ids):
            idxs = np.where(class_ids == c)[0]
            keep = self._nms(boxes[idxs], scores[idxs], self.iou_thres)
            final_indices.extend(idxs[kk] for kk in keep)

        for i in final_indices:
            self.draw_detections(img, boxes[i], scores[i], int(class_ids[i]))

        return img

    def detect(self, img_path: str) -> np.ndarray:
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"Unable to read image: {img_path}")

        inp, pad = self.preprocess(img)

        input_index = self.input_details[0]["index"]
        if self.input_details[0]["dtype"] == np.uint8 and "quantization" in self.input_details[0]:
            zero_point = self.input_details[0]["quantization_parameters"].get(
                "zero_points", [0])
            scale = self.input_details[0]["quantization_parameters"].get("scales", [
                                                                         1.0])
            if len(scale) == 1 and len(zero_point) == 1:
                inp_q = (inp / float(scale[0]) +
                         float(zero_point[0])).astype(np.uint8)
            else:
                inp_q = inp.astype(np.uint8)
            self.interpreter.set_tensor(input_index, inp_q)
        else:
            self.interpreter.set_tensor(
                input_index, inp.astype(self.input_details[0]["dtype"]))

        self.interpreter.invoke()

        output_tensors = []
        for od in self.output_details:
            output_tensors.append(self.interpreter.get_tensor(od["index"]))
        outputs = output_tensors[0] if len(
            output_tensors) == 1 else output_tensors

        result = self.postprocess(img.copy(), outputs, pad)
        return result
