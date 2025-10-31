from typing import Optional, Union, Tuple, List
import os
import json
import numpy as np
import cv2

try:
    from tflite_runtime.interpreter import Interpreter
except Exception:
    try:
        from tensorflow.lite import Interpreter  # type: ignore
    except Exception as e:
        Interpreter = None  # type: ignore


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
        if Interpreter is None:
            raise RuntimeError(
                "No TFLite Interpreter available. Install tflite_runtime or TensorFlow.")

        self.model = model
        self.conf = float(conf)
        self.iou = float(iou)
        self.metadata = metadata

        # Load class names
        self.names: List[str] = self._load_class_names(
            metadata) if metadata else self._default_coco_names()

        # Colors for drawing (deterministic per class id)
        rng = np.random.default_rng(0xC0C0)
        self.colors = (rng.random((max(1, len(self.names)), 3))
                       * 255).astype(np.uint8)

        # Create interpreter
        self.interpreter = Interpreter(model_path=self.model)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        # Assume single input
        in_det = self.input_details[0]
        self.input_index = in_det["index"]
        self.input_dtype = in_det["dtype"]
        self.input_quant = in_det.get("quantization", (0.0, 0))
        in_shape = in_det["shape"]
        # NHWC expected
        if len(in_shape) != 4:
            raise ValueError(f"Unexpected input shape: {in_shape}")
        self.batch, self.inp_h, self.inp_w, self.inp_c = int(
            in_shape[0]), int(in_shape[1]), int(in_shape[2]), int(in_shape[3])
        if self.batch != 1:
            raise ValueError("Only batch size 1 is supported.")
        self.is_quantized = (self.input_dtype == np.uint8)

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        '''Resizes and reshapes images while maintaining aspect ratio by adding padding, suitable for YOLO models.'''
        h, w = img.shape[:2]
        new_h, new_w = int(new_shape[0]), int(new_shape[1])
        r = min(new_h / h, new_w / w)

        unpad_w, unpad_h = int(round(w * r)), int(round(h * r))
        dw = (new_w - unpad_w) / 2
        dh = (new_h - unpad_h) / 2

        if (w, h) != (unpad_w, unpad_h):
            img = cv2.resize(img, (unpad_w, unpad_h),
                             interpolation=cv2.INTER_LINEAR)

        top, bottom = int(np.floor(dh)), int(np.ceil(dh))
        left, right = int(np.floor(dw)), int(np.ceil(dw))

        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
        return img, (dh, dw)

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
        x, y, w, h = box.astype(int).tolist()
        x2, y2 = x + w, y + h
        color = tuple(int(c)
                      for c in self.colors[class_id % len(self.colors)].tolist())
        cv2.rectangle(img, (x, y), (x2, y2), color, 2)
        label = f"{self.names[class_id] if 0 <= class_id < len(self.names) else class_id}: {float(score):.2f}"
        t_w, t_h = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)[0]
        cv2.rectangle(img, (x, y - t_h - 6), (x + t_w + 4, y), color, -1)
        cv2.putText(img, label, (x + 2, y - 4), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (255, 255, 255), 1, cv2.LINE_AA)

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
        img_resized, (dh, dw) = self.letterbox(img, (self.inp_h, self.inp_w))
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)

        if self.is_quantized:
            scale, zero_point = self.input_quant if self.input_quant is not None else (
                1.0, 0)
            # Convert to [0,1] then quantize
            x = img_rgb.astype(np.float32) / 255.0
            x = np.round(x / (scale if scale != 0 else 1.0) +
                         zero_point).clip(0, 255).astype(np.uint8)
        else:
            x = img_rgb.astype(np.float32) / 255.0

        x = np.expand_dims(x, axis=0)
        return x, (dh, dw)

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
        orig_h, orig_w = img.shape[:2]
        dh, dw = pad
        r = min(self.inp_h / orig_h, self.inp_w / orig_w)

        # Flatten outputs list if necessary
        if isinstance(outputs, (list, tuple)):
            outs = outputs
        else:
            outs = [outputs]

        # Try to detect NMS-style outputs: boxes, classes, scores, num
        boxes_arr = None
        classes_arr = None
        scores_arr = None
        num_arr = None

        for arr in outs:
            a = np.squeeze(arr)
            if a.ndim == 2 and a.shape[-1] == 4:
                boxes_arr = a  # (N, 4) typically [ymin, xmin, ymax, xmax]
            elif a.ndim == 1 and a.size <= 300 and np.issubdtype(a.dtype, np.integer):
                classes_arr = a  # (N,)
            elif a.ndim == 1 and a.size <= 300 and np.issubdtype(a.dtype, np.floating):
                # Could be scores or num
                if a.size == 1:
                    num_arr = a
                else:
                    # Heuristic: scores between 0..1
                    if np.all((a >= 0) & (a <= 1.0)):
                        scores_arr = a
            elif a.ndim == 0 and np.issubdtype(a.dtype, np.integer):
                num_arr = a

        detections: List[Tuple[int, float, np.ndarray]] = []

        if boxes_arr is not None and scores_arr is not None and classes_arr is not None:
            # NMS already applied by model
            n = int(num_arr.item()
                    ) if num_arr is not None else boxes_arr.shape[0]
            n = min(n, boxes_arr.shape[0],
                    scores_arr.shape[0], classes_arr.shape[0])

            for i in range(n):
                score = float(scores_arr[i])
                if score < self.conf:
                    continue
                cls_id = int(classes_arr[i])
                y1, x1, y2, x2 = boxes_arr[i].tolist()

                # Determine if normalized
                if 0.0 <= x1 <= 1.5 and 0.0 <= y1 <= 1.5 and 0.0 <= x2 <= 1.5 and 0.0 <= y2 <= 1.5:
                    # denormalize to input dims
                    x1 *= self.inp_w
                    x2 *= self.inp_w
                    y1 *= self.inp_h
                    y2 *= self.inp_h

                # Undo letterbox
                x1 = (x1 - dw) / r
                y1 = (y1 - dh) / r
                x2 = (x2 - dw) / r
                y2 = (y2 - dh) / r

                # Clip
                x1 = max(0.0, min(x1, orig_w - 1))
                y1 = max(0.0, min(y1, orig_h - 1))
                x2 = max(0.0, min(x2, orig_w - 1))
                y2 = max(0.0, min(y2, orig_h - 1))

                w = max(0.0, x2 - x1)
                h = max(0.0, y2 - y1)
                box_xywh = np.array([x1, y1, w, h], dtype=np.float32)
                detections.append((cls_id, score, box_xywh))
        else:
            # Raw predictions (no NMS in graph). Expect shape (N, M) where first 4 are xywh and rest classes (+ maybe objectness)
            # Pick the largest output tensor as predictions
            pred = max((np.squeeze(a) for a in outs), key=lambda t: t.size)
            if pred.ndim == 3:
                # e.g., (1, 8400, 84) squeezed to (8400, 84)
                pred = np.squeeze(pred)
            if pred.ndim != 2:
                return img

            # Determine layout: [x,y,w,h, obj?, cls...]
            n_col = pred.shape[1]
            if n_col >= 6:
                # If there is obj conf, assume col 4 is obj, else no obj
                # Heuristic: if sum of cols 5.. end about 1.0 per row after sigmoid in TFLite; we apply sigmoid if values beyond range
                # Apply sigmoid to confidences if out of 0..1 range
                arr = pred.astype(np.float32)
                # Sigmoid where necessary

                def sigmoid(x):
                    return 1.0 / (1.0 + np.exp(-x))

                # Detect if logits (values outside [0,1])
                if np.any(arr[:, 4:] > 1.0) or np.any(arr[:, 4:] < 0.0):
                    arr[:, 4:] = sigmoid(arr[:, 4:])

                if n_col - 5 > 0:
                    obj = arr[:, 4]
                    cls_scores = arr[:, 5:]
                else:
                    obj = np.ones((arr.shape[0],), dtype=np.float32)
                    cls_scores = arr[:, 4:]

                cls_ids = np.argmax(cls_scores, axis=1)
                cls_conf = cls_scores[np.arange(cls_scores.shape[0]), cls_ids]
                confs = obj * cls_conf

                # Filter by confidence
                keep = confs >= self.conf
                arr = arr[keep]
                confs = confs[keep]
                cls_ids = cls_ids[keep]

                if arr.size == 0:
                    return img

                # Convert xywh to xyxy
                x_c, y_c, w_b, h_b = arr[:, 0], arr[:, 1], arr[:, 2], arr[:, 3]

                # Determine if normalized
                normalized = np.all((x_c <= 1.5) & (y_c <= 1.5) & (
                    w_b <= 1.5) & (h_b <= 1.5) & (x_c >= 0) & (y_c >= 0))
                if normalized:
                    x_c *= self.inp_w
                    y_c *= self.inp_h
                    w_b *= self.inp_w
                    h_b *= self.inp_h

                x1 = x_c - w_b / 2.0
                y1 = y_c - h_b / 2.0
                x2 = x_c + w_b / 2.0
                y2 = y_c + h_b / 2.0

                # Undo letterbox
                x1 = (x1 - dw) / r
                y1 = (y1 - dh) / r
                x2 = (x2 - dw) / r
                y2 = (y2 - dh) / r

                # Clip
                x1 = np.clip(x1, 0, orig_w - 1)
                y1 = np.clip(y1, 0, orig_h - 1)
                x2 = np.clip(x2, 0, orig_w - 1)
                y2 = np.clip(y2, 0, orig_h - 1)

                boxes_xywh = np.stack(
                    [x1, y1, np.maximum(0.0, x2 - x1), np.maximum(0.0, y2 - y1)], axis=1)

                # NMS
                indices = self._nms_cv2(boxes_xywh, confs, self.iou)
                for idx in indices:
                    detections.append(
                        (int(cls_ids[idx]), float(confs[idx]), boxes_xywh[idx]))
            else:
                return img

        # Draw detections
        for cls_id, score, box_xywh in detections:
            self.draw_detections(img, box_xywh, np.float32(score), cls_id)
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
            raise FileNotFoundError(f"Image not found: {img_path}")
        img0 = cv2.imread(img_path, cv2.IMREAD_COLOR)
        if img0 is None:
            raise ValueError(f"Failed to read image: {img_path}")

        x, pad = self.preprocess(img0)
        # Set input tensor
        self.interpreter.set_tensor(self.input_index, x)
        self.interpreter.invoke()
        # Get outputs
        outputs = [self.interpreter.get_tensor(
            o["index"]) for o in self.output_details]
        out_img = self.postprocess(img0.copy(), outputs, pad)
        return out_img

    def _nms_cv2(self, boxes_xywh: np.ndarray, scores: np.ndarray, iou_thres: float) -> List[int]:
        b = boxes_xywh.astype(np.float32)
        s = scores.astype(np.float32).tolist()
        boxes = b[:, :4]
        # cv2.dnn.NMSBoxes expects [x, y, w, h]
        try:
            idxs = cv2.dnn.NMSBoxes(bboxes=boxes.tolist(
            ), scores=s, score_threshold=self.conf, nms_threshold=iou_thres)
            if isinstance(idxs, (list, tuple)):
                idxs = [int(i) for i in idxs]
            elif isinstance(idxs, np.ndarray):
                idxs = idxs.flatten().astype(int).tolist()
            else:
                idxs = []
        except Exception:
            # Fallback to simple NMS
            idxs = self._nms_numpy_xywh(boxes, scores, iou_thres)
        return idxs

    def _nms_numpy_xywh(self, boxes: np.ndarray, scores: np.ndarray, iou_thres: float) -> List[int]:
        if boxes.size == 0:
            return []
        x = boxes[:, 0]
        y = boxes[:, 1]
        w = boxes[:, 2]
        h = boxes[:, 3]
        x2 = x + w
        y2 = y + h

        order = scores.argsort()[::-1]
        keep: List[int] = []
        while order.size > 0:
            i = int(order[0])
            keep.append(i)

            xx1 = np.maximum(x[i], x[order[1:]])
            yy1 = np.maximum(y[i], y[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            inter_w = np.maximum(0.0, xx2 - xx1)
            inter_h = np.maximum(0.0, yy2 - yy1)
            inter = inter_w * inter_h
            area_i = w[i] * h[i]
            area_rest = w[order[1:]] * h[order[1:]]
            union = area_i + area_rest - inter
            iou = np.where(union > 0, inter / union, 0.0)

            inds = np.where(iou <= iou_thres)[0]
            order = order[inds + 1]
        return keep

    def _load_class_names(self, path: str) -> List[str]:
        names: List[str] = []
        if not os.path.isfile(path):
            return self._default_coco_names()
        try:
            # Try JSON
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                if "names" in data:
                    if isinstance(data["names"], list):
                        names = [str(x) for x in data["names"]]
                    elif isinstance(data["names"], dict):
                        names = [data["names"][k] for k in sorted(
                            data["names"].keys(), key=lambda x: int(x) if str(x).isdigit() else x)]
            elif isinstance(data, list):
                names = [str(x) for x in data]
        except Exception:
            # Try YAML
            try:
                import yaml  # type: ignore
                with open(path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                if isinstance(data, dict) and "names" in data:
                    if isinstance(data["names"], list):
                        names = [str(x) for x in data["names"]]
                    elif isinstance(data["names"], dict):
                        names = [data["names"][k] for k in sorted(
                            data["names"].keys(), key=lambda x: int(x) if str(x).isdigit() else x)]
            except Exception:
                # Try plain text (one name per line)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        names = [line.strip() for line in f if line.strip()]
                except Exception:
                    names = []
        if not names:
            names = self._default_coco_names()
        return names

    def _default_coco_names(self) -> List[str]:
        return [
            "person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light",
            "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
            "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie", "suitcase", "frisbee",
            "skis", "snowboard", "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
            "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
            "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
            "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse", "remote", "keyboard",
            "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase",
            "scissors", "teddy bear", "hair drier", "toothbrush"
        ]
