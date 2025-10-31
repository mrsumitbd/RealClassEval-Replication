import cv2
import numpy as np
import torch

class TensorCLAHE:

    def __init__(self):
        self.clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))

    def __call__(self, tensor):
        img_np = tensor.permute(1, 2, 0).numpy() * 255
        img_np = img_np.astype(np.uint8)
        channels = cv2.split(img_np)
        clahe_channels = [self.clahe.apply(ch) for ch in channels]
        clahe_image_np = cv2.merge(clahe_channels)
        tensor = torch.from_numpy(clahe_image_np).float() / 255.0
        return tensor.permute(2, 0, 1)