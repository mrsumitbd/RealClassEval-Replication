
import numpy as np
import cv2
from typing import Tuple, Union, Optional
import tensorflow as tf
import json
import os


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
        '''
        self.model_path = model
        self.conf = conf
        self.iou = iou
        self.metadata = metadata
        self.interpreter = tf.lite.Interpreter(model_path=self.model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.input_shape = self.input_details[0]['shape'][1:3]
        self.class_names = None
        if self.metadata is not None and os.path.exists(self.metadata):
            with open(self.metadata, 'r') as f:
                meta = json.load(f)
                if 'names' in meta:
                    self.class_names = meta['names']
                elif 'class_names' in meta:
                    self.class_names = meta['class_names']
        if self.class_names is None:
            # Default COCO 80 classes
            self.class_names = [
                'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light',
                'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
                'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee',
                'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard',
                'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
                'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch',
                'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard',
                'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase',
                'scissors', 'teddy bear', 'hair drier', 'toothbrush'
            ]

    def letterbox(self, img: np.ndarray, new_shape: Tuple = (640, 640)) -> Tuple[np.ndarray, Tuple[float, float]]:
        '''Resizes and reshapes images while maintaining aspect ratio by adding padding, suitable for YOLO models.'''
        shape = img.shape[:2]  # current shape [height, width]
        ratio = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        new_unpad = (int(round(shape[1] * ratio)),
                     int(round(shape[0] * ratio)))
        dw = new_shape[1] - new_unpad[0]
        dh = new_shape[0] - new_unpad[1]
        dw /= 2  # divide padding into 2 sides
        dh /= 2

        img = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)
        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
        img = cv2.copyMakeBorder(
            img, top, bottom, left, right, cv2.BORDER_CONSTANT, value=(114, 114, 114))
        return img, (ratio, dw, dh)

    def draw_detections(self, img: np.ndarray, box: np.ndarray, score: np.float32, class_id: int) -> None:
        '''
        Draws bounding boxes and labels on the input image based on the detected objects.
        '''
        x1, y1, w, h = box.astype(int)
        x2, y2 = x1 + w, y1 + h
        color = (0, 255, 0)
        label = f"{self.class_names[class_id]}: {score:.2f}"
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        (tw, th), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(img, (x1, y1 - th - 4), (x1 + tw, y1), color, -1)
        cv2.putText(img, label, (x1, y1 - 2),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def preprocess(self, img: np.ndarray) -> Tuple[np.ndarray, Tuple[float, float]]:
        '''
        Preprocesses the input image before performing inference.
        '''
        img0 = img.copy()
        img, (ratio, dw, dh) = self.letterbox(img0, self.input_shape)
        img = img.astype(np.float32)
        img /= 255.0
        img = np.expand_dims(img, axis=0)
        return img, (ratio, dw, dh)

    def nms(self, boxes, scores, iou_threshold):
        '''Performs Non-Maximum Suppression and returns indices of kept boxes.'''
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 0] + boxes[:, 2]
        y2 = boxes[:, 1] + boxes[:, 3]
        areas = (x2 - x1) * (y2 - y1)
        order = scores.argsort()[::-1]
        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            w = np.maximum(0.0, xx2 - xx1)
            h = np.maximum(0.0, yy2 - yy1)
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter)
            inds = np.where(ovr <= iou_threshold)[0]
            order = order[inds + 1]
        return keep

    def postprocess(self, img: np.ndarray, outputs: np.ndarray, pad: Tuple[float, float]) -> np.ndarray:
        '''
        Performs post-processing on the model's output to extract bounding boxes, scores, and class IDs.
        '''
        ratio, dw, dh = pad
        h0, w0 = img.shape[:2]
        # YOLOv8 TFLite output: (1, N, 6) or (1, N, 85) [x, y, w, h, conf, class scores...]
        if outputs.ndim == 3:
            outputs = outputs[0]
        if outputs.shape[1] > 6:
            # [x, y, w, h, obj_conf, class_scores...]
            boxes = outputs[:, :4]
            obj_conf = outputs[:, 4:5]
            class_scores = outputs[:, 5:]
            class_ids = np.argmax(class_scores, axis=1)
            scores = obj_conf[:, 0] * \
                class_scores[np.arange(class_scores.shape[0]), class_ids]
        else:
            # [x, y, w, h, conf, class_id]
            boxes = outputs[:, :4]
            scores = outputs[:, 4]
            class_ids = outputs[:, 5].astype(int)
        # Filter by confidence
        mask = scores > self.conf
        boxes = boxes[mask]
        scores = scores[mask]
        class_ids = class_ids[mask]
        if len(boxes) == 0:
            return img
        # Convert boxes from [cx, cy, w, h] to [x1, y1, w, h] and rescale to original image
        boxes_xy = np.zeros_like(boxes)
        boxes_xy[:, 0] = boxes[:, 0] - boxes[:, 2] / 2  # x1
        boxes_xy[:, 1] = boxes[:, 1] - boxes[:, 3] / 2  # y1
        boxes_xy[:, 2] = boxes[:, 2]
        boxes_xy[:, 3] = boxes[:, 3]
        # Undo letterbox and scale to original image
        boxes_xy[:, 0] = (boxes_xy[:, 0] - dw) / ratio
        boxes_xy[:, 1] = (boxes_xy[:, 1] - dh) / ratio
        boxes_xy[:, 2] = boxes_xy[:, 2] / ratio
        boxes_xy[:, 3] = boxes_xy[:, 3] / ratio
        # Clip boxes
        boxes_xy[:, 0] = np.clip(boxes_xy[:, 0], 0, w0 - 1)
        boxes_xy[:, 1] = np.clip(boxes_xy[:, 1], 0, h0 - 1)
        boxes_xy[:, 2] = np.clip(boxes_xy[:, 2], 0, w0 - boxes_xy[:, 0])
        boxes_xy[:, 3] = np.clip(boxes_xy[:, 3], 0, h0 - boxes_xy[:, 1])
        # NMS
        keep = self.nms(boxes_xy, scores, self.iou)
        for i in keep:
            self.draw_detections(
                img, boxes_xy[i], scores[i], int(class_ids[i]))
        return img

    def detect(self, img_path: str) -> np.ndarray:
        '''
        Performs inference using a TFLite model and returns the output image with drawn detections.
        '''
        img0 = cv2.imread(img_path)
        if img0 is None:
            raise FileNotFoundError(f"Image not found: {img_path}")
        img_input, pad = self.preprocess(img0)
        input_index = self.input_details[0]['index']
        if self.input_details[0]['dtype'] == np.uint8:
            img_input = (img_input * 255).astype(np.uint8)
        self.interpreter.set_tensor(input_index, img_input)
        self.interpreter.invoke()
        output_index = self.output_details[0]['index']
        outputs = self.interpreter.get_tensor(output_index)
        img_out = img0.copy()
        img_out = self.postprocess(img_out, outputs, pad)
        return img_out
