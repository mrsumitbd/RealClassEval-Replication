import cv2
from PIL import Image
import numpy as np

class CLAHE:
    """Contrast Limited Adaptive Histogram Equalization."""

    def __init__(self):
        self.clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))

    def __call__(self, image):
        image_np = np.array(image)
        if len(image_np.shape) == 3:
            channels = cv2.split(image_np)
            clahe_channels = [self.clahe.apply(ch) for ch in channels]
            clahe_image_np = cv2.merge(clahe_channels)
        else:
            clahe_image_np = self.clahe.apply(image_np)
        clahe_image = Image.fromarray(clahe_image_np)
        return clahe_image