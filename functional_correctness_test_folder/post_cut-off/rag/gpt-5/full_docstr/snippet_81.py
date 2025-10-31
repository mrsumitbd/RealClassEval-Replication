import os
import json
import yaml
import cv2
import numpy as np
from typing import Tuple, Union, Optional, List, Dict


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
        self.model = model
        self.conf = float(conf)
        self.iou = float(iou)
        self.metadata = metadata

        try:
            from tflite_runtime.interpreter import Interpreter
        except Exception:
            from tensorflow.lite import Interpreter  # type: ignore

        self.interpreter = Interpreter(model_path=self.model)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        in_shape = self.input_details[0]['shape']
        # Expect [1, h, w, 3]
        if len(in_shape) != 4:
            raise RuntimeError('Unsupported input shape for TFLite model.')
        self.in_height = int(in_shape[1])
        self.in_width = int(in_shape[2])
        self.in_channels = int(in_shape[3])
        self.input_dtype = self.input_details[0]['dtype']
        self.input_quant = self.input_details[0].get('quantization', (0.0, 0))
        self.output_quants = [od.get('quantization', (0.0, 0))
                              for od in self.output_details]

        self.class_names = self._load_class_names(self.metadata)
        self.num_classes = len(self.class_names) if self.class_names else 0
        self.colors = self._build_colors(self.num_classes or 80)

    def _load_class_names(self, metadata_path: Optional[str]) -> List[str]:
        names: List[str] = []
        if metadata_path is None:
            return names
        if not os.path.isfile(metadata_path):
            return names
        ext = os.path.splitext(metadata_path)[1].lower()
        try:
            if ext in ('.yaml', '.yml'):
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if isinstance(data, dict):
                        if 'names' in data and isinstance(data['names'], (list, tuple)):
                            names = [str(x) for x in data['names']]
                        elif 'classes' in data and isinstance(data['classes'], (list, tuple)):
                            names = [str(x) for x in data['classes']]
            elif ext == '.json':
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        if 'names' in data and isinstance(data['names'], (list, tuple)):
                            names = [str(x) for x in data['names']]
                        elif 'classes' in data and isinstance(data['classes'], (list, tuple)):
                            names = [str(x) for x in data['classes']]
                    elif isinstance(data, list):
                        names = [str(x) for x in data]
            else:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            names.append(line)
        except Exception:
            names = []
        return names

    def _build_colors(self, n: int) -> List[Tuple[int, int, int]]:
        rng = np.random.RandomState(42)
        cols = []
        for i in range(n):
            c = rng.randint(0, 255, size=3).tolist()
            cols.append((int(c[0]), int(c[1]), int(c[2])))
        return cols

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        '''Resizes and reshapes images while maintaining aspect ratio by adding padding, suitable for YOLO models.'''
        shape = img.shape[:2]  # (h, w)
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)
        new_h, new_w = int(new_shape[0]), int(new_shape[1])

        r = min(new_h / shape[0], new_w / shape[1])
        scaled = (int(round(shape[1] * r)), int(round(shape[0] * r)))  # (w, h)

        dw = new_w - scaled[0]
        dh = new_h - scaled[1]

        dw /= 2
        dh /= 2

        if scaled != (shape[1], shape[0]):
            img = cv2.resize(
                img, (scaled[0], scaled[1]), interpolation=cv2.INTER_LINEAR)

        top = int(round(dh - 0.1))
        bottom = int(round(dh + 0.1))
        left = int(round(dw - 0.1))
        right = int(round(dw + 0.1))

        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
        return img, (float(left), float(top))

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
        x1, y1, w, h = box.astype(int).tolist()
        x2, y2 = x1 + w, y1 + h
        color = self.colors[class_id % len(self.colors)]
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        if self.class_names and 0 <= class_id < len(self.class_names):
            label = f'{self.class_names[class_id]} {float(score):.2f}'
        else:
            label = f'{class_id} {float(score):.2f}'
        (tw, th), bl = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        th = max(th, 12)
        cv2.rectangle(img, (x1, y1 - th - 4), (x1 + tw + 2, y1), color, -1)
        cv2.putText(img, label, (x1 + 1, y1 - 4), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), thickness=1, lineType=cv2.LINE_AA)

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
        if img.ndim == 2:
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        if img.shape[2] == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lb_img, pad = self.letterbox(rgb, (self.in_height, self.in_width))
        inp = lb_img

        if self.input_dtype == np.float32:
            inp = inp.astype(np.float32) / 255.0
        elif self.input_dtype == np.uint8:
            # If quantized input, the interpreter expects uint8 values. Leave as is.
            inp = inp.astype(np.uint8)
        else:
            inp = inp.astype(self.input_dtype)

        inp = np.expand_dims(inp, axis=0)  # [1, h, w, 3]
        if self.input_dtype != np.uint8 and self.input_quant and self.input_quant[0] not in (0.0, None):
            scale, zero = self.input_quant
            inp = np.clip(np.round(inp / scale + zero),
                          0, 255).astype(np.uint8)

        return inp, pad

    def _dequantize(self, arr: np.ndarray, quant: Tuple[float, int]) -> np.ndarray:
        scale, zero = quant if quant is not None else (0.0, 0)
        if scale and scale != 0.0:
            return (arr.astype(np.float32) - float(zero)) * float(scale)
        return arr.astype(np.float32)

    def _to_candidates(self, out: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        # Normalize output to shape (N, M) where columns contain [x,y,w,h,(obj),class...]
        arr = out
        if arr.ndim == 3 and arr.shape[0] == 1:
            arr = arr[0]
        if arr.ndim == 2 and arr.shape[0] in (84, 85, 116, 117):  # (M, N)
            arr = arr.transpose(1, 0)
        if arr.ndim != 2:
            arr = arr.reshape((-1, arr.shape[-1]))

        M = arr.shape[1]
        # Determine format
        # Prefer with obj conf if available
        if M > 5:
            nc_85 = M - 5
            nc_84 = M - 4
            use_obj = nc_85 > 0 and (
                self.num_classes in (0, nc_85) or nc_85 <= 1000)
            if use_obj:
                boxes = arr[:, 0:4]
                obj = arr[:, 4:5]
                cls_scores = arr[:, 5:]
                cls_id = np.argmax(cls_scores, axis=1)
                cls_prob = cls_scores[np.arange(cls_scores.shape[0]), cls_id]
                scores = cls_prob * obj.flatten()
            else:
                boxes = arr[:, 0:4]
                cls_scores = arr[:, 4:]
                cls_id = np.argmax(cls_scores, axis=1)
                scores = cls_scores[np.arange(cls_scores.shape[0]), cls_id]
        else:
            # Unexpected
            return np.zeros((0, 4), dtype=np.float32), np.zeros((0,), dtype=np.float32), np.zeros((0,), dtype=np.int32)

        # Convert xywh(center) -> xyxy
        cx, cy, w, h = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
        x1 = cx - w / 2
        y1 = cy - h / 2
        x2 = cx + w / 2
        y2 = cy + h / 2
        xyxy = np.stack([x1, y1, x2, y2], axis=1).astype(np.float32)

        return xyxy, scores.astype(np.float32), cls_id.astype(np.int32)

    def _nms(self, boxes: np.ndarray, scores: np.ndarray, iou_thres: float) -> List[int]:
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        areas = (x2 - x1).clip(min=0) * (y2 - y1).clip(min=0)
        order = scores.argsort()[::-1]
        keep: List[int] = []
        while order.size > 0:
            i = order[0]
            keep.append(int(i))
            if order.size == 1:
                break
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            w = (xx2 - xx1).clip(min=0)
            h = (yy2 - yy1).clip(min=0)
            inter = w * h
            iou = inter / (areas[i] + areas[order[1:]] - inter + 1e-6)
            inds = np.where(iou <= iou_thres)[0]
            order = order[inds + 1]
        return keep

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
        # Retrieve combined output
        out_tensors: List[np.ndarray] = []
        if isinstance(outputs, (list, tuple)):
            out_tensors = list(outputs)
        else:
            out_tensors = [outputs]

        # If model exposes multiple outputs as boxes, scores, classes
        boxes_scored = False
        det_boxes = None
        det_scores = None
        det_classes = None

        if len(out_tensors) >= 3:
            # Try to detect conventional (N,4), (N,), (N,)
            cand = []
            for i, od in enumerate(self.output_details[:len(out_tensors)]):
                arr = out_tensors[i]
                arr = self._dequantize(arr, self.output_quants[i])
                cand.append(arr)
            shapes = [c.squeeze().shape for c in cand]
            flat = [c.squeeze() for c in cand]
            try:
                # boxes
                b = flat[0]
                s = flat[1]
                c = flat[2]
                if b.ndim == 2 and b.shape[1] == 4 and s.ndim in (1, 2) and c.ndim in (1, 2):
                    if s.ndim == 2 and s.shape[1] == 1:
                        s = s[:, 0]
                    if c.ndim == 2 and c.shape[1] == 1:
                        c = c[:, 0]
                    if b.shape[0] == s.shape[0] == c.shape[0]:
                        det_boxes = b.astype(np.float32)
                        det_scores = s.astype(np.float32)
                        det_classes = c.astype(np.int32)
                        boxes_scored = True
            except Exception:
                boxes_scored = False

        if not boxes_scored:
            # Use single prediction tensor or fallback
            arr = self._dequantize(out_tensors[0], self.output_quants[0])
            xyxy, scores, cls_id = self._to_candidates(arr)
        else:
            # Convert [ymin, xmin, ymax, xmax] -> xyxy if necessary
            b = det_boxes
            if b.shape[1] == 4:
                # Assume xyxy if x1<x2 and y1<y2 majority; otherwise yxyx
                sample = b[:min(10, len(b))]
                xy_wise = np.mean(sample[:, 2] > sample[:, 0]) > 0.5 and np.mean(
                    sample[:, 3] > sample[:, 1]) > 0.5
                if xy_wise:
                    xyxy = b
                else:
                    xyxy = np.stack(
                        [b[:, 1], b[:, 0], b[:, 3], b[:, 2]], axis=1)
            else:
                xyxy = b[:, :4]
            scores = det_scores
            cls_id = det_classes

        # Filter by conf
        m = scores >= self.conf
        xyxy = xyxy[m]
        scores = scores[m]
        cls_id = cls_id[m]

        if xyxy.size == 0:
            return img

        # Map boxes back to original image
        h0, w0 = img.shape[:2]
        r = min(self.in_height / float(h0), self.in_width / float(w0))
        pad_w, pad_h = pad  # left, top
        # reverse letterbox
        # xyxy are on the letterboxed image scale (input dims). Subtract pad then divide by r.
        xyxy[:, [0, 2]] -= pad_w
        xyxy[:, [1, 3]] -= pad_h
        xyxy[:, [0, 2]] /= r
        xyxy[:, [1, 3]] /= r

        # Clip to image
        xyxy[:, 0] = np.clip(xyxy[:, 0], 0, w0 - 1)
        xyxy[:, 1] = np.clip(xyxy[:, 1], 0, h0 - 1)
        xyxy[:, 2] = np.clip(xyxy[:, 2], 0, w0 - 1)
        xyxy[:, 3] = np.clip(xyxy[:, 3], 0, h0 - 1)

        # NMS per class
        final_inds: List[int] = []
        for c in np.unique(cls_id):
            inds = np.where(cls_id == c)[0]
            keep = self._nms(xyxy[inds], scores[inds], self.iou)
            final_inds.extend(inds[keep])
        final_inds = list(
            sorted(set(final_inds), key=lambda i: float(scores[i]), reverse=True))

        for i in final_inds:
            x1, y1, x2, y2 = xyxy[i]
            w = max(0.0, x2 - x1)
            h = max(0.0, y2 - y1)
            self.draw_detections(img, np.array(
                [x1, y1, w, h], dtype=np.float32), scores[i], int(cls_id[i]))

        return img

    def detect(self, img_path: str) -> np.ndarray:
        '''
        Performs inference using a TFLite model and returns the output image with drawn detections.
        Args:
            img_path (str): The path to the input image file.
        Returns:
            np.ndarray: The output image with drawn detections.
        '''
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        if img is None:
            raise FileNotFoundError(f'Image not found: {img_path}')
        inp, pad = self.preprocess(img)

        idx = self.input_details[0]['index']
        self.interpreter.set_tensor(idx, inp)
        self.interpreter.invoke()

        outputs: List[np.ndarray] = []
        for od in self.output_details:
            out = self.interpreter.get_tensor(od['index'])
            outputs.append(out)

        if len(outputs) == 1:
            annotated = self.postprocess(img.copy(), outputs[0], pad)
        else:
            annotated = self.postprocess(img.copy(), outputs, pad)
        return annotated
