
import numpy as np


class Blend:

    def overlay(self, img1, img2):
        img1 = img1.astype(np.float32) / 255.0
        img2 = img2.astype(np.float32) / 255.0
        result = np.where(img1 <= 0.5, 2 * img1 * img2,
                          1 - 2 * (1 - img1) * (1 - img2))
        result = np.clip(result * 255, 0, 255).astype(np.uint8)
        return result

    def hue(self, img1, img2):
        def rgb_to_hsv(img):
            return np.array([np.vectorize(lambda r, g, b: tuple(np.array([*colorsys.rgb_to_hsv(r, g, b)])))(*img[..., i].transpose(2, 0, 1)) for i in range(img.shape[0])]).transpose(1, 2, 0, 3)

        def hsv_to_rgb(img):
            return np.array([np.vectorize(lambda h, s, v: tuple(np.array([*colorsys.hsv_to_rgb(h, s, v)])))(*img[..., i].transpose(2, 0, 1)) for i in range(img.shape[0])]).transpose(1, 2, 0, 3)
        import colorsys
        img1f = img1.astype(np.float32) / 255.0
        img2f = img2.astype(np.float32) / 255.0
        hsv1 = np.zeros_like(img1f)
        hsv2 = np.zeros_like(img2f)
        for i in range(img1.shape[0]):
            for j in range(img1.shape[1]):
                hsv1[i, j] = colorsys.rgb_to_hsv(*img1f[i, j])
                hsv2[i, j] = colorsys.rgb_to_hsv(*img2f[i, j])
        out = np.zeros_like(img1f)
        for i in range(img1.shape[0]):
            for j in range(img1.shape[1]):
                h = hsv2[i, j, 0]
                s = hsv1[i, j, 1]
                v = hsv1[i, j, 2]
                out[i, j] = colorsys.hsv_to_rgb(h, s, v)
        out = np.clip(out * 255, 0, 255).astype(np.uint8)
        return out

    def color(self, img1, img2):
        import colorsys
        img1f = img1.astype(np.float32) / 255.0
        img2f = img2.astype(np.float32) / 255.0
        hsv1 = np.zeros_like(img1f)
        hsv2 = np.zeros_like(img2f)
        for i in range(img1.shape[0]):
            for j in range(img1.shape[1]):
                hsv1[i, j] = colorsys.rgb_to_hsv(*img1f[i, j])
                hsv2[i, j] = colorsys.rgb_to_hsv(*img2f[i, j])
        out = np.zeros_like(img1f)
        for i in range(img1.shape[0]):
            for j in range(img1.shape[1]):
                h = hsv1[i, j, 0]
                s = hsv1[i, j, 1]
                v = hsv2[i, j, 2]
                out[i, j] = colorsys.hsv_to_rgb(h, s, v)
        out = np.clip(out * 255, 0, 255).astype(np.uint8)
        return out
