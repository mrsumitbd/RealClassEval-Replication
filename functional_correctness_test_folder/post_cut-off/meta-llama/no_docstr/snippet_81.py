
import numpy as np
from typing import Tuple, Union
import cv2
import tflite_runtime.interpreter as tflite


class YOLOv8TFLite:

    def __init__(self, model: str, conf: float = 0.25, iou: float = 0.45, metadata: Union[str, None] = None):
        self.interpreter = tflite.Interpreter(model_path=model)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.conf_threshold = conf
        self.iou_threshold = iou
        self.metadata = metadata

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        shape = img.shape[:2]  # current shape [height, width]
        if isinstance(new_shape, int):
            new_shape = (new_shape, new_shape)

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        # Compute padding
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - \
            new_unpad[1]  # wh padding

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(img, top, bottom, left, right,
                                 cv2.BORDER_CONSTANT, value=(114, 114, 114))  # add border

        return img, (r, (dw, dh))

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:
        x1, y1, x2, y2 = map(int, box)
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        label = f'Class {class_id}: {score:.2f}'
        cv2.putText(img, label, (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img, pad = self.letterbox(img)
        img = img.transpose((2, 0, 1))  # HWC to CHW
        img = np.expand_dims(img, axis=0)  # Add batch dimension
        img = np.ascontiguousarray(img, dtype=np.float32) / 255.0
        return img, pad

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        r, (dw, dh) = pad
        outputs = np.squeeze(outputs)
        outputs[:, :4] -= np.array([dw, dh, dw, dh])
        outputs[:, :4] /= r
        outputs[:, 0] = np.clip(outputs[:, 0], 0, img.shape[1])
        outputs[:, 1] = np.clip(outputs[:, 1], 0, img.shape[0])
        outputs[:, 2] = np.clip(outputs[:, 2], 0, img.shape[1])
        outputs[:, 3] = np.clip(outputs[:, 3], 0, img.shape[0])
        conf_mask = outputs[:, 4:] > self.conf_threshold
        scores = outputs[:, 4:]
        class_ids = np.argmax(scores, axis=1)
        scores = np.max(scores, axis=1)
        mask = conf_mask[np.arange(len(conf_mask)), class_ids]
        boxes = outputs[:, :4][mask]
        scores = scores[mask]
        class_ids = class_ids[mask]
        indices = cv2.dnn.NMSBoxes(
            boxes.tolist(), scores.tolist(), self.conf_threshold, self.iou_threshold)
        if indices is not None:
            indices = np.array(indices).flatten()
            boxes = boxes[indices]
            scores = scores[indices]
            class_ids = class_ids[indices]
            detections = np.hstack(
                (boxes, scores[:, None], class_ids[:, None]))
        else:
            detections = np.zeros((0, 6))
        return detections

    def detect(self, img_path: str) -> np.ndarray:
        img = cv2.imread(img_path)
        img_pre, pad = self.preprocess(img)
        self.interpreter.set_tensor(self.input_details[0]['index'], img_pre)
        self.interpreter.invoke()
        outputs = self.interpreter.get_tensor(self.output_details[0]['index'])
        detections = self.postprocess(img, outputs, pad)
        for det in detections:
            self.draw_detections(img, det[:4], det[4], int(det[5]))
        return detections
