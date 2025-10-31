
from PIL import Image
import numpy as np


class Blend:
    def _ensure_rgba(self, img):
        return img.convert("RGBA")

    def _resize_to(self, img, size):
        if img.size != size:
            return img.resize(size, Image.BICUBIC)
        return img

    def overlay(self, img1, img2):
        """Applies the overlay blend mode.
        Overlays image img2 on image img1. The overlay pixel combines
        multiply and screen: it multiplies dark pixels values and screen
        light values. Returns a composite image with the alpha channel
        retained.
        """
        img1 = self._ensure_rgba(img1)
        img2 = self._ensure_rgba(self._resize_to(img2, img1.size))

        a1 = np.array(img1, dtype=np.float32)
        a2 = np.array(img2, dtype=np.float32)

        # Separate RGB and alpha
        rgb1, alpha1 = a1[..., :3], a1[..., 3]
        rgb2 = a2[..., :3]

        # Overlay formula
        mask = rgb2 <= 128
        out_rgb = np.empty_like(rgb1)
        out_rgb[mask] = 2 * rgb1[mask] * rgb2[mask] / 255
        out_rgb[~mask] = 255 - 2 * \
            (255 - rgb1[~mask]) * (255 - rgb2[~mask]) / 255

        out_rgb = np.clip(out_rgb, 0, 255).astype(np.uint8)
        out_alpha = alpha1.astype(np.uint8)

        out = np.dstack((out_rgb, out_alpha))
        return Image.fromarray(out, mode="RGBA")

    def hue(self, img1, img2):
        """Applies the hue blend mode.
        Hues image img1 with image img2. The hue filter replaces the
        hues of pixels in img1 with the hues of pixels in img2. Returns
        a composite image with the alpha channel retained.
        """
        img1 = self._ensure_rgba(img1)
        img2 = self._ensure_rgba(self._resize_to(img2, img1.size))

        # Convert to HSV
        hsv1 = img1.convert("HSV")
        hsv2 = img2.convert("HSV")

        h1, s1, v1 = np.array(hsv1, dtype=np.uint8).transpose(2, 0, 1)
        h2, s2, v2 = np.array(hsv2, dtype=np.uint8).transpose(2, 0, 1)

        # Replace hue
        h_new = h2
        s_new = s1
        v_new = v1

        hsv_new = np.dstack((h_new, s_new, v_new)).transpose(
            1, 2, 0).astype(np.uint8)
        rgb_new = Image.fromarray(hsv_new, mode="HSV").convert("RGB")

        # Preserve alpha from img1
        alpha = np.array(img1, dtype=np.uint8)[..., 3]
        out = np.dstack((np.array(rgb_new), alpha))
        return Image.fromarray(out, mode="RGBA")

    def color(self, img1, img2):
        """Applies the color blend mode.
        Replaces the hue and saturation of img1 with those of img2,
        keeping the value (brightness) of img1. Returns a composite
        image with the alpha channel retained.
        """
        img1 = self._ensure_rgba(img1)
        img2 = self._ensure_rgba(self._resize_to(img2, img1.size))

        # Convert to HSV
        hsv1 = img1.convert("HSV")
        hsv2 = img2.convert("HSV")

        h1, s1, v1 = np.array(hsv1, dtype=np.uint8).transpose(2, 0, 1)
        h2, s2, v2 = np.array(hsv2, dtype=np.uint8).transpose(2, 0, 1)

        # Replace hue and saturation
        h_new = h2
        s_new = s2
        v_new = v1

        hsv_new = np.dstack((h_new, s_new, v_new)).transpose(
            1, 2, 0).astype(np.uint8)
        rgb_new = Image.fromarray(hsv_new, mode="HSV").convert("RGB")

        # Preserve alpha from img1
        alpha = np.array(img1, dtype=np.uint8)[..., 3]
        out = np.dstack((np.array(rgb_new), alpha))
        return Image.fromarray(out, mode="RGBA")
