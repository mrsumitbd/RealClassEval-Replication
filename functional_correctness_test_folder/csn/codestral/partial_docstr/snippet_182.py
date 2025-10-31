
import numpy as np
from PIL import Image


class Blend:

    def overlay(self, img1, img2):
        img1 = np.array(img1)
        img2 = np.array(img2)

        mask = img2 / 255.0 > 0.5
        img2 = np.where(mask, 255 - (255 - img2) *
                        (255 - img1) / 255, img1 * img2 / 255)
        img2 = img2.astype(np.uint8)

        return Image.fromarray(img2)

    def hue(self, img1, img2):
        img1 = np.array(img1)
        img2 = np.array(img2)

        hsv1 = np.array(Image.fromarray(img1).convert('HSV'))
        hsv2 = np.array(Image.fromarray(img2).convert('HSV'))

        hsv1[:, :, 0] = hsv2[:, :, 0]

        img2 = np.array(Image.fromarray(hsv1).convert('RGB'))

        return Image.fromarray(img2)

    def color(self, img1, img2):
        img1 = np.array(img1)
        img2 = np.array(img2)

        hsv1 = np.array(Image.fromarray(img1).convert('HSV'))
        hsv2 = np.array(Image.fromarray(img2).convert('HSV'))

        hsv1[:, :, 0] = hsv2[:, :, 0]
        hsv1[:, :, 1] = hsv2[:, :, 1]

        img2 = np.array(Image.fromarray(hsv1).convert('RGB'))

        return Image.fromarray(img2)
