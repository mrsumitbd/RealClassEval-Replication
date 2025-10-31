
import numpy as np


class Blend:

    def overlay(self, img1, img2):
        if img1.shape != img2.shape:
            raise ValueError("Images must have the same dimensions")

        result = np.zeros_like(img1, dtype=np.float32)
        for i in range(img1.shape[0]):
            for j in range(img1.shape[1]):
                for k in range(img1.shape[2]):
                    a = img1[i, j, k] / 255.0
                    b = img2[i, j, k] / 255.0
                    if a <= 0.5:
                        result[i, j, k] = 2 * a * b * 255
                    else:
                        result[i, j, k] = (1 - 2 * (1 - a) * (1 - b)) * 255
        return np.clip(result, 0, 255).astype(np.uint8)

    def hue(self, img1, img2):
        if img1.shape != img2.shape:
            raise ValueError("Images must have the same dimensions")

        hsv1 = self._rgb_to_hsv(img1)
        hsv2 = self._rgb_to_hsv(img2)
        hsv_result = np.dstack((hsv2[:, :, 0], hsv1[:, :, 1], hsv1[:, :, 2]))
        return self._hsv_to_rgb(hsv_result)

    def color(self, img1, img2):
        if img1.shape != img2.shape:
            raise ValueError("Images must have the same dimensions")

        hsv1 = self._rgb_to_hsv(img1)
        hsv2 = self._rgb_to_hsv(img2)
        hsv_result = np.dstack((hsv2[:, :, 0], hsv2[:, :, 1], hsv1[:, :, 2]))
        return self._hsv_to_rgb(hsv_result)

    def _rgb_to_hsv(self, img):
        img = img.astype(np.float32) / 255.0
        r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]

        max_val = np.max(img, axis=2)
        min_val = np.min(img, axis=2)
        delta = max_val - min_val

        h = np.zeros_like(max_val)
        s = np.zeros_like(max_val)
        v = max_val

        mask = delta != 0
        s[mask] = delta[mask] / max_val[mask]

        mask_r = (max_val == r) & mask
        mask_g = (max_val == g) & mask
        mask_b = (max_val == b) & mask

        h[mask_r] = (g[mask_r] - b[mask_r]) / delta[mask_r] % 6
        h[mask_g] = (b[mask_g] - r[mask_g]) / delta[mask_g] + 2
        h[mask_b] = (r[mask_b] - g[mask_b]) / delta[mask_b] + 4

        h = (h / 6) % 1.0
        hsv = np.dstack((h, s, v))
        return hsv

    def _hsv_to_rgb(self, hsv):
        h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

        h = (h * 6.0) % 6.0
        i = np.floor(h).astype(np.uint8)
        f = h - i
        p = v * (1 - s)
        q = v * (1 - s * f)
        t = v * (1 - s * (1 - f))

        rgb = np.zeros_like(hsv)
        rgb[i == 0] = np.dstack((v[i == 0], t[i == 0], p[i == 0]))
        rgb[i == 1] = np.dstack((q[i == 1], v[i == 1], p[i == 1]))
        rgb[i == 2] = np.dstack((p[i == 2], v[i == 2], t[i == 2]))
        rgb[i == 3] = np.dstack((p[i == 3], q[i == 3], v[i == 3]))
        rgb[i == 4] = np.dstack((t[i == 4], p[i == 4], v[i == 4]))
        rgb[i == 5] = np.dstack((v[i == 5], p[i == 5], q[i == 5]))

        rgb = np.clip(rgb * 255, 0, 255).astype(np.uint8)
        return rgb
