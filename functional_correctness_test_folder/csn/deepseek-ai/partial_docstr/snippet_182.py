
import numpy as np
from PIL import Image


class Blend:

    def overlay(self, img1, img2):
        '''Applies the overlay blend mode.
        Overlays image img2 on image img1. The overlay pixel combines
        multiply and screen: it multiplies dark pixels values and screen
        light values. Returns a composite image with the alpha channel
        retained.
        '''
        img1_arr = np.array(img1, dtype=np.float32) / 255.0
        img2_arr = np.array(img2, dtype=np.float32) / 255.0

        if img1_arr.shape[2] == 4 or img2_arr.shape[2] == 4:
            alpha1 = img1_arr[:, :, 3] if img1_arr.shape[2] == 4 else np.ones_like(
                img1_arr[:, :, 0])
            alpha2 = img2_arr[:, :, 3] if img2_arr.shape[2] == 4 else np.ones_like(
                img2_arr[:, :, 0])
            alpha = np.maximum(alpha1, alpha2)

        result = np.where(img1_arr[:, :, :3] < 0.5,
                          2 * img1_arr[:, :, :3] * img2_arr[:, :, :3],
                          1 - 2 * (1 - img1_arr[:, :, :3]) * (1 - img2_arr[:, :, :3]))

        result = np.clip(result, 0, 1)

        if img1_arr.shape[2] == 4 or img2_arr.shape[2] == 4:
            result = np.dstack((result, alpha[:, :, np.newaxis]))

        return Image.fromarray((result * 255).astype(np.uint8))

    def hue(self, img1, img2):
        '''Applies the hue blend mode.
        Hues image img1 with image img2. The hue filter replaces the
        hues of pixels in img1 with the hues of pixels in img2. Returns
        a composite image with the alpha channel retained.
        '''
        img1_arr = np.array(img1, dtype=np.float32) / 255.0
        img2_arr = np.array(img2, dtype=np.float32) / 255.0

        if img1_arr.shape[2] == 4 or img2_arr.shape[2] == 4:
            alpha1 = img1_arr[:, :, 3] if img1_arr.shape[2] == 4 else np.ones_like(
                img1_arr[:, :, 0])
            alpha2 = img2_arr[:, :, 3] if img2_arr.shape[2] == 4 else np.ones_like(
                img2_arr[:, :, 0])
            alpha = np.maximum(alpha1, alpha2)

        hsv1 = self._rgb_to_hsv(img1_arr[:, :, :3])
        hsv2 = self._rgb_to_hsv(img2_arr[:, :, :3])

        hsv_result = np.dstack((hsv2[:, :, 0], hsv1[:, :, 1], hsv1[:, :, 2]))
        rgb_result = self._hsv_to_rgb(hsv_result)

        if img1_arr.shape[2] == 4 or img2_arr.shape[2] == 4:
            rgb_result = np.dstack((rgb_result, alpha[:, :, np.newaxis]))

        return Image.fromarray((rgb_result * 255).astype(np.uint8))

    def color(self, img1, img2):
        '''Applies the color blend mode.
        Colors image img1 with image img2. The color filter replaces the
        hue and saturation of pixels in img1 with the hue and saturation
        of pixels in img2. Returns a composite image with the alpha channel
        retained.
        '''
        img1_arr = np.array(img1, dtype=np.float32) / 255.0
        img2_arr = np.array(img2, dtype=np.float32) / 255.0

        if img1_arr.shape[2] == 4 or img2_arr.shape[2] == 4:
            alpha1 = img1_arr[:, :, 3] if img1_arr.shape[2] == 4 else np.ones_like(
                img1_arr[:, :, 0])
            alpha2 = img2_arr[:, :, 3] if img2_arr.shape[2] == 4 else np.ones_like(
                img2_arr[:, :, 0])
            alpha = np.maximum(alpha1, alpha2)

        hsv1 = self._rgb_to_hsv(img1_arr[:, :, :3])
        hsv2 = self._rgb_to_hsv(img2_arr[:, :, :3])

        hsv_result = np.dstack((hsv2[:, :, 0], hsv2[:, :, 1], hsv1[:, :, 2]))
        rgb_result = self._hsv_to_rgb(hsv_result)

        if img1_arr.shape[2] == 4 or img2_arr.shape[2] == 4:
            rgb_result = np.dstack((rgb_result, alpha[:, :, np.newaxis]))

        return Image.fromarray((rgb_result * 255).astype(np.uint8))

    def _rgb_to_hsv(self, rgb):
        max_val = np.max(rgb, axis=2)
        min_val = np.min(rgb, axis=2)
        delta = max_val - min_val

        h = np.zeros_like(max_val)
        mask = delta != 0

        r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]

        h[max_val == r] = (g[max_val == r] - b[max_val == r]
                           ) / delta[max_val == r] % 6
        h[max_val == g] = (b[max_val == g] - r[max_val == g]
                           ) / delta[max_val == g] + 2
        h[max_val == b] = (r[max_val == b] - g[max_val == b]
                           ) / delta[max_val == b] + 4

        h = (h / 6) % 1.0
        s = np.where(max_val == 0, 0, delta / max_val)
        v = max_val

        return np.dstack((h, s, v))

    def _hsv_to_rgb(self, hsv):
        h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

        c = v * s
        x = c * (1 - np.abs((h * 6) % 2 - 1))
        m = v - c

        rgb_prime = np.zeros_like(hsv)

        mask = (0 <= h) & (h < 1/6)
        rgb_prime[mask] = np.dstack((c[mask], x[mask], np.zeros_like(c[mask])))

        mask = (1/6 <= h) & (h < 2/6)
        rgb_prime[mask] = np.dstack((x[mask], c[mask], np.zeros_like(c[mask])))

        mask = (2/6 <= h) & (h < 3/6)
        rgb_prime[mask] = np.dstack((np.zeros_like(c[mask]), c[mask], x[mask])))

        mask = (3/6 <= h) & (h < 4/6)
        rgb_prime[mask] = np.dstack((np.zeros_like(c[mask]), x[mask], c[mask])))

        mask = (4/6 <= h) & (h < 5/6)
        rgb_prime[mask] = np.dstack((x[mask], np.zeros_like(c[mask]), c[mask])))

        mask = (5/6 <= h) & (h < 1)
        rgb_prime[mask] = np.dstack((c[mask], np.zeros_like(c[mask]), x[mask])))

        rgb = (rgb_prime + m[:, :, np.newaxis])
        return np.clip(rgb, 0, 1)
