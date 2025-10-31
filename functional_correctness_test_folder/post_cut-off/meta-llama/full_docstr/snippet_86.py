
import numpy as np


class Instances:
    def __init__(self, bbox, labels):
        self.bbox = bbox
        self.labels = labels

    def __len__(self):
        return len(self.bbox)

    def __getitem__(self, index):
        return Instances(self.bbox[index], self.labels[index])


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
            raise ValueError("Image not provided")

        # Get the image shape
        h, w = image.shape[:2]

        # Determine the new shape
        if self.auto:
            r = min(self.new_shape[0] / h, self.new_shape[1] / w)
        else:
            r = min(self.new_shape[0] / h, self.new_shape[1] / w) if not self.scaleFill else max(
                self.new_shape[0] / h, self.new_shape[1] / w)

        if not self.scaleup:
            r = min(r, 1.0)

        new_unpad = (int(round(w * r)), int(round(h * r)))
        dw, dh = self.new_shape[1] - \
            new_unpad[0], self.new_shape[0] - new_unpad[1]

        if self.center:
            dw /= 2
            dh /= 2

        # Resize the image
        if r != 1:
            image = np.ascontiguousarray(np.resize(image, (new_unpad[1], new_unpad[0], image.shape[2])) if len(
                image.shape) == 3 else np.resize(image, (new_unpad[1], new_unpad[0])))

        # Pad the image
        top, bottom = int(round(dh - 0.1)) if self.center else 0, int(
            round(dh + 0.1)) if self.center else int(round(dh))
        left, right = int(round(dw - 0.1)) if self.center else 0, int(
            round(dw + 0.1)) if self.center else int(round(dw))
        image = np.pad(image, ((top, bottom), (left, right), (0, 0)) if len(image.shape) == 3 else (
            (top, bottom), (left, right)), mode='constant', constant_values=114)

        # Ensure the image size is divisible by stride
        h, w = image.shape[:2]
        new_h, new_w = (h + self.stride - 1) // self.stride * \
            self.stride, (w + self.stride - 1) // self.stride * self.stride
        if (h, w) != (new_h, new_w):
            image = np.pad(image, ((0, new_h - h), (0, new_w - w), (0, 0)) if len(image.shape)
                           == 3 else ((0, new_h - h), (0, new_w - w)), mode='constant', constant_values=114)

        if "instances" in labels:
            labels = self._update_labels(labels, (r, r), left, top)

        labels["img"] = image
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
        instances.bbox[:, 0] = instances.bbox[:, 0] * ratio[0] + padw
        instances.bbox[:, 1] = instances.bbox[:, 1] * ratio[1] + padh
        instances.bbox[:, 2] = instances.bbox[:, 2] * ratio[0] + padw
        instances.bbox[:, 3] = instances.bbox[:, 3] * ratio[1] + padh
        labels["instances"] = instances
        return labels


# Example usage
if __name__ == "__main__":
    letterbox = LetterBox(new_shape=(640, 640))
    image = np.random.rand(480, 640, 3)
    instances = Instances(
        np.array([[10, 10, 20, 20], [30, 30, 40, 40]]), np.array([0, 1]))
    labels = {"img": image, "instances": instances}
    result = letterbox(labels)
    resized_img = result["img"]
    updated_instances = result["instances"]
    print(resized_img.shape)
    print(updated_instances.bbox)
