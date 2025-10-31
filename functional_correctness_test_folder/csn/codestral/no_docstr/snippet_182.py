
import numpy as np


class Blend:

    def overlay(self, img1, img2):
        img1 = img1.astype(float)
        img2 = img2.astype(float)
        result = np.where(img2 <= 128, 2 * img1 * img2 / 255,
                          255 - 2 * (255 - img1) * (255 - img2) / 255)
        return result.astype(np.uint8)

    def hue(self, img1, img2):
        img1_hsv = np.array(img1, dtype=np.float32)
        img2_hsv = np.array(img2, dtype=np.float32)
        img1_hsv = cv2.cvtColor(img1_hsv, cv2.COLOR_RGB2HSV)
        img2_hsv = cv2.cvtColor(img2_hsv, cv2.COLOR_RGB2HSV)
        img1_hsv[:, :, 0] = img2_hsv[:, :, 0]
        result = cv2.cvtColor(img1_hsv, cv2.COLOR_HSV2RGB)
        return result.astype(np.uint8)

    def color(self, img1, img2):
        img1_hsv = np.array(img1, dtype=np.float32)
        img2_hsv = np.array(img2, dtype=np.float32)
        img1_hsv = cv2.cvtColor(img1_hsv, cv2.COLOR_RGB2HSV)
        img2_hsv = cv2.cvtColor(img2_hsv, cv2.COLOR_RGB2HSV)
        img1_hsv[:, :, 1:] = img2_hsv[:, :, 1:]
        result = cv2.cvtColor(img1_hsv, cv2.COLOR_HSV2RGB)
        return result.astype(np.uint8)
