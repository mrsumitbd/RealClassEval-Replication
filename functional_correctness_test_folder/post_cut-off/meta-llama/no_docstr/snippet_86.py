
import numpy as np


class Instances:
    def __init__(self, bbox, labels=None, masks=None, keypoints=None):
        self.bbox = bbox
        self.labels = labels
        self.masks = masks
        self.keypoints = keypoints

    def __repr__(self):
        return f"Instances(bbox={self.bbox}, labels={self.labels}, masks={self.masks}, keypoints={self.keypoints})"


class LetterBox:
    '''
    Resize image and padding for detection, instance segmentation, pose.
    This class resizes and pads images to a specified shape while preserving aspect ratio. It also updates
    corresponding labels and bounding boxes.
    Attributes:
        new_shape (tuple): Target shape (height, width) for resizing.
        auto (bool): Whether to use minimum rectangle.
        scaleFill (bool): Whether to stretch the image to new_shape.
        scaleup (bool): Whether to allow scaling up. If False, only scale down.
        stride (int): Stride for rounding padding.
        center (bool): Whether to center the image or align to top-left.
    Methods:
        __call__: Resize and pad image, update labels and bounding boxes.
    Examples:
        >>> transform = LetterBox(new_shape=(640, 640))
        >>> result = transform(labels)
        >>> resized_img = result["img"]
        >>> updated_instances = result["instances"]
    '''

    def __init__(self, new_shape=(640, 640), auto=False, scaleFill=False, scaleup=True, center=True, stride=32):
        '''
        Initialize LetterBox object for resizing and padding images.
        This class is designed to resize and pad images for object detection, instance segmentation, and pose estimation
        tasks. It supports various resizing modes including auto-sizing, scale-fill, and letterboxing.
        Args:
            new_shape (Tuple[int, int]): Target size (height, width) for the resized image.
            auto (bool): If True, use minimum rectangle to resize. If False, use new_shape directly.
            scaleFill (bool): If True, stretch the image to new_shape without padding.
            scaleup (bool): If True, allow scaling up. If False, only scale down.
            center (bool): If True, center the placed image. If False, place image in top-left corner.
            stride (int): Stride of the model (e.g., 32 for YOLOv5).
        Attributes:
            new_shape (Tuple[int, int]): Target size for the resized image.
            auto (bool): Flag for using minimum rectangle resizing.
            scaleFill (bool): Flag for stretching image without padding.
            scaleup (bool): Flag for allowing upscaling.
            stride (int): Stride value for ensuring image size is divisible by stride.
        Examples:
            >>> letterbox = LetterBox(new_shape=(640, 640), auto=False, scaleFill=False, scaleup=True, stride=32)
            >>> resized_img = letterbox(original_img)
        '''
        self.new_shape = new_shape
        self.auto = auto
        self.scaleFill = scaleFill
        self.scaleup = scaleup
        self.stride = stride
        self.center = center

    def __call__(self, labels=None, image=None):
        '''
        Resizes and pads an image for object detection, instance segmentation, or pose estimation tasks.
        This method applies letterboxing to the input image, which involves resizing the image while maintaining its
        aspect ratio and adding padding to fit the new shape. It also updates any associated labels accordingly.
        Args:
            labels (Dict | None): A dictionary containing image data and associated labels, or empty dict if None.
            image (np.ndarray | None): The input image as a numpy array. If None, the image is taken from 'labels'.
        Returns:
            (Dict | Tuple): If 'labels' is provided, returns an updated dictionary with the resized and padded image,
                updated labels, and additional metadata. If 'labels' is empty, returns a tuple containing the resized
                and padded image, and a tuple of (ratio, (left_pad, top_pad)).
        Examples:
            >>> letterbox = LetterBox(new_shape=(640, 640))
            >>> result = letterbox(labels={"img": np.zeros((480, 640, 3)), "instances": Instances(...)})
            >>> resized_img = result["img"]
            >>> updated_instances = result["instances"]
        '''
        if labels is None:
            labels = {}
        if image is None:
            image = labels.get("img")

        if image is None:
            raise ValueError("Either 'labels' or 'image' must be provided")

        shape = image.shape[:2]  # current shape [height, width]
        new_shape = self.new_shape

        # Scale ratio (new / old)
        r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
        # only scale down, do not scale up (for better test mAP)
        if not self.scaleup:
            r = min(r, 1.0)

        # Compute padding
        ratio = r, r  # width, height ratios
        new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
        dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - \
            new_unpad[1]  # wh padding
        if self.auto:  # minimum rectangle
            dw, dh = np.mod(dw, self.stride), np.mod(
                dh, self.stride)  # wh padding
        elif self.scaleFill:  # stretch
            dw, dh = 0.0, 0.0
            new_unpad = (new_shape[1], new_shape[0])
            ratio = new_shape[1] / shape[1], new_shape[0] / \
                shape[0]  # width, height ratios

        dw /= 2  # divide padding into 2 sides
        dh /= 2

        if shape[::-1] != new_unpad:  # resize
            image = np.ascontiguousarray(
                np.resize(image, new_unpad + (image.shape[2],)))

        top, bottom = int(
            round(dh - 0.1)) if self.center else 0, int(round(dh + 0.1))
        left, right = int(
            round(dw - 0.1)) if self.center else 0, int(round(dw + 0.1))
        image = np.pad(image, ((top, bottom), (left, right),
                       (0, 0)), mode='constant', constant_values=114)

        if "img" in labels:
            labels["img"] = image
        if "instances" in labels:
            labels = self._update_labels(labels, ratio, left, top)

        if len(labels) == 0:
            return image, (ratio, (left, top))
        return labels

    @staticmethod
    def _update_labels(labels, ratio, padw, padh):
        '''
        Updates labels after applying letterboxing to an image.
        This method modifies the bounding box coordinates of instances in the labels
        to account for resizing and padding applied during letterboxing.
        Args:
            labels (Dict): A dictionary containing image labels and instances.
            ratio (Tuple[float, float]): Scaling ratios (width, height) applied to the image.
            padw (float): Padding width added to the image.
            padh (float): Padding height added to the image.
        Returns:
            (Dict): Updated labels dictionary with modified instance coordinates.
        Examples:
            >>> letterbox = LetterBox(new_shape=(640, 640))
            >>> labels = {"instances": Instances(...)}
            >>> ratio = (0.5, 0.5)
            >>> padw, padh = 10, 20
            >>> updated_labels = letterbox._update_labels(labels, ratio, padw, padh)
        '''
        instances = labels["instances"]
        instances.bbox[:, 0] = ratio[0] * instances.bbox[:, 0] + padw
        instances.bbox[:, 1] = ratio[1] * instances.bbox[:, 1] + padh
        instances.bbox[:, 2] = ratio[0] * instances.bbox[:, 2] + padw
        instances.bbox[:, 3] = ratio[1] * instances.bbox[:, 3] + padh
        if instances.keypoints is not None:
            instances.keypoints[..., 0] = ratio[0] * \
                instances.keypoints[..., 0] + padw
            instances.keypoints[..., 1] = ratio[1] * \
                instances.keypoints[..., 1] + padh
        if instances.masks is not None:
            # Assuming masks are represented as polygons or binary masks
            # For simplicity, let's assume it's a binary mask
            # In real scenarios, you might need to adjust this based on your mask representation
            instances.masks = np.ascontiguousarray(np.resize(instances.masks, (instances.masks.shape[0], int(
                instances.masks.shape[1] * ratio[1]), int(instances.masks.shape[2] * ratio[0]))))
            pad = ((0, 0), (padh, padh), (padw, padw))
            instances.masks = np.pad(
                instances.masks, pad, mode='constant', constant_values=0)
        labels["instances"] = instances
        return labels


# Example usage
if __name__ == "__main__":
    letterbox = LetterBox(new_shape=(640, 640))
    img = np.random.rand(480, 640, 3)
    instances = Instances(bbox=np.array([[10, 10, 50, 50]]))
    labels = {"img": img, "instances": instances}
    result = letterbox(labels)
    print(result["img"].shape)
    print(result["instances"].bbox)
