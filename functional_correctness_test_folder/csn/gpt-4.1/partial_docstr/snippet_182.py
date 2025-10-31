
import numpy as np
from PIL import Image


class Blend:

    def overlay(self, img1, img2):
        '''Applies the overlay blend mode.'''
        arr1 = np.array(img1).astype(np.float32) / 255.0
        arr2 = np.array(img2).astype(np.float32) / 255.0

        rgb1 = arr1[..., :3]
        rgb2 = arr2[..., :3]
        alpha1 = arr1[..., 3:4]
        alpha2 = arr2[..., 3:4]

        mask = rgb1 <= 0.5
        out_rgb = np.zeros_like(rgb1)
        out_rgb[mask] = 2 * rgb1[mask] * rgb2[mask]
        out_rgb[~mask] = 1 - 2 * (1 - rgb1[~mask]) * (1 - rgb2[~mask])

        out_alpha = alpha1 * alpha2 + alpha1 * \
            (1 - alpha2) + alpha2 * (1 - alpha1)
        out = np.concatenate([out_rgb, out_alpha], axis=-1)
        out = np.clip(out * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(out, 'RGBA')

    def hue(self, img1, img2):
        '''Applies the hue blend mode.'''
        arr1 = np.array(img1).astype(np.float32) / 255.0
        arr2 = np.array(img2).astype(np.float32) / 255.0

        rgb1 = arr1[..., :3]
        rgb2 = arr2[..., :3]
        alpha1 = arr1[..., 3:4]
        alpha2 = arr2[..., 3:4]

        def rgb_to_hsv(rgb):
            return np.array([colorsys.rgb_to_hsv(*pixel) for pixel in rgb.reshape(-1, 3)]).reshape(rgb.shape)

        def hsv_to_rgb(hsv):
            return np.array([colorsys.hsv_to_rgb(*pixel) for pixel in hsv.reshape(-1, 3)]).reshape(hsv.shape)

        import colorsys
        hsv1 = rgb_to_hsv(rgb1)
        hsv2 = rgb_to_hsv(rgb2)
        new_hsv = np.stack([hsv2[..., 0], hsv1[..., 1], hsv1[..., 2]], axis=-1)
        out_rgb = hsv_to_rgb(new_hsv)

        out_alpha = alpha1 * alpha2 + alpha1 * \
            (1 - alpha2) + alpha2 * (1 - alpha1)
        out = np.concatenate([out_rgb, out_alpha], axis=-1)
        out = np.clip(out * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(out, 'RGBA')

    def color(self, img1, img2):
        '''Applies the color blend mode.'''
        arr1 = np.array(img1).astype(np.float32) / 255.0
        arr2 = np.array(img2).astype(np.float32) / 255.0

        rgb1 = arr1[..., :3]
        rgb2 = arr2[..., :3]
        alpha1 = arr1[..., 3:4]
        alpha2 = arr2[..., 3:4]

        def rgb_to_hsv(rgb):
            return np.array([colorsys.rgb_to_hsv(*pixel) for pixel in rgb.reshape(-1, 3)]).reshape(rgb.shape)

        def hsv_to_rgb(hsv):
            return np.array([colorsys.hsv_to_rgb(*pixel) for pixel in hsv.reshape(-1, 3)]).reshape(hsv.shape)

        import colorsys
        hsv1 = rgb_to_hsv(rgb1)
        hsv2 = rgb_to_hsv(rgb2)
        new_hsv = np.stack([hsv2[..., 0], hsv2[..., 1], hsv1[..., 2]], axis=-1)
        out_rgb = hsv_to_rgb(new_hsv)

        out_alpha = alpha1 * alpha2 + alpha1 * \
            (1 - alpha2) + alpha2 * (1 - alpha1)
        out = np.concatenate([out_rgb, out_alpha], axis=-1)
        out = np.clip(out * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(out, 'RGBA')
