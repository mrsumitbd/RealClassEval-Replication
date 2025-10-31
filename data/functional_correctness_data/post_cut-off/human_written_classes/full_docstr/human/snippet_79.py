from ultralytics.utils import ASSETS, yaml_load
import cv2
import numpy as np
from ultralytics.utils.checks import check_requirements, check_yaml
import onnxruntime as ort

class RTDETR:
    """RTDETR object detection model class for handling inference and visualization."""

    def __init__(self, model_path, img_path, conf_thres=0.5, iou_thres=0.5):
        """
        Initializes the RTDETR object with the specified parameters.

        Args:
            model_path: Path to the ONNX model file.
            img_path: Path to the input image.
            conf_thres: Confidence threshold for object detection.
            iou_thres: IoU threshold for non-maximum suppression
        """
        self.model_path = model_path
        self.img_path = img_path
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.session = ort.InferenceSession(model_path, providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
        self.model_input = self.session.get_inputs()
        self.input_width = self.model_input[0].shape[2]
        self.input_height = self.model_input[0].shape[3]
        self.classes = yaml_load(check_yaml('coco8.yaml'))['names']
        self.color_palette = np.random.uniform(0, 255, size=(len(self.classes), 3))

    def draw_detections(self, box, score, class_id):
        """
        Draws bounding boxes and labels on the input image based on the detected objects.

        Args:
            box: Detected bounding box.
            score: Corresponding detection score.
            class_id: Class ID for the detected object.

        Returns:
            None
        """
        x1, y1, x2, y2 = box
        color = self.color_palette[class_id]
        cv2.rectangle(self.img, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        label = f'{self.classes[class_id]}: {score:.2f}'
        (label_width, label_height), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        label_x = x1
        label_y = y1 - 10 if y1 - 10 > label_height else y1 + 10
        cv2.rectangle(self.img, (int(label_x), int(label_y - label_height)), (int(label_x + label_width), int(label_y + label_height)), color, cv2.FILLED)
        cv2.putText(self.img, label, (int(label_x), int(label_y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)

    def preprocess(self):
        """
        Preprocesses the input image before performing inference.

        Returns:
            image_data: Preprocessed image data ready for inference.
        """
        self.img = cv2.imread(self.img_path)
        self.img_height, self.img_width = self.img.shape[:2]
        img = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (self.input_width, self.input_height))
        image_data = np.array(img) / 255.0
        image_data = np.transpose(image_data, (2, 0, 1))
        image_data = np.expand_dims(image_data, axis=0).astype(np.float32)
        return image_data

    def bbox_cxcywh_to_xyxy(self, boxes):
        """
        Converts bounding boxes from (center x, center y, width, height) format to (x_min, y_min, x_max, y_max) format.

        Args:
            boxes (numpy.ndarray): An array of shape (N, 4) where each row represents
                                a bounding box in (cx, cy, w, h) format.

        Returns:
            numpy.ndarray: An array of shape (N, 4) where each row represents
                        a bounding box in (x_min, y_min, x_max, y_max) format.
        """
        half_width = boxes[:, 2] / 2
        half_height = boxes[:, 3] / 2
        x_min = boxes[:, 0] - half_width
        y_min = boxes[:, 1] - half_height
        x_max = boxes[:, 0] + half_width
        y_max = boxes[:, 1] + half_height
        return np.column_stack((x_min, y_min, x_max, y_max))

    def postprocess(self, model_output):
        """
        Postprocesses the model output to extract detections and draw them on the input image.

        Args:
            model_output: Output of the model inference.

        Returns:
            np.array: Annotated image with detections.
        """
        outputs = np.squeeze(model_output[0])
        boxes = outputs[:, :4]
        scores = outputs[:, 4:]
        labels = np.argmax(scores, axis=1)
        scores = np.max(scores, axis=1)
        mask = scores > self.conf_thres
        boxes, scores, labels = (boxes[mask], scores[mask], labels[mask])
        boxes = self.bbox_cxcywh_to_xyxy(boxes)
        boxes[:, 0::2] *= self.img_width
        boxes[:, 1::2] *= self.img_height
        for box, score, label in zip(boxes, scores, labels):
            self.draw_detections(box, score, label)
        return self.img

    def main(self):
        """
        Executes the detection on the input image using the ONNX model.

        Returns:
            np.array: Output image with annotations.
        """
        image_data = self.preprocess()
        model_output = self.session.run(None, {self.model_input[0].name: image_data})
        return self.postprocess(model_output)