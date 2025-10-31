
import cv2
import numpy as np


class Blend:
    def _check_shape(self, img1, img2):
        if img1.shape != img2.shape:
            raise ValueError("Images must have the same shape")
        if img1.dtype != np.uint8 or img2.dtype != np.uint8:
            raise ValueError("Images must be of type uint8")

    def overlay(self, img1, img2):
        """
        Overlay blend mode.
        """
        self._check_shape(img1, img2)
        # Convert to float for computation
        a = img1.astype(np.float32) / 255.0
        b = img2.astype(np.float32) / 255.0

        # Overlay formula
        out = np.where(a < 0.5,
                       2 * a * b,
                       1 - 2 * (1 - a) * (1 - b))

        out = (out * 255).clip(0, 255).astype(np.uint8)
        return out

    def hue(self, img1, img2):
        """
        Hue blend mode: replace hue of img1 with hue of img2.
        """
        self._check_shape(img1, img2)
        hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV).astype(np.float32)

        # Replace hue channel
        hsv1[..., 0] = hsv2[..., 0]
        # Convert back to BGR
        out = cv2.cvtColor(hsv1.astype(np.uint8), cv2.COLOR_HSV2BGR)
        return out

    def color(self, img1, img2):
        """
        Color blend mode: replace saturation and value of img1 with those of img2.
        """
        self._check_shape(img1, img2)
        hsv1 = cv2.cvtColor(img1, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv2 = cv2.cvtColor(img2, cv2.COLOR_BGR2HSV).astype(np.float32)

        # Replace saturation and value channels
        hsv1[..., 1] = hsv2[..., 1]
        hsv1[..., 2] = hsv2[..., 2]
        # Convert back to BGR
        out = cv2.cvtColor(hsv1.astype(np.uint8), cv2.COLOR_HSV2BGR)
        return out
