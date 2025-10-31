
from PIL import Image
import numpy as np
import colorsys


class Blend:
    '''Layer blending modes.
    Implements additional blending modes to those present in PIL.
    These blending functions can not be used separately from
    the canvas.flatten() method, where the alpha compositing
    of two layers is handled.
    Since these blending are not part of a C library,
    but pure Python, they take forever to process.
    '''

    def overlay(self, img1, img2):
        '''Applies the overlay blend mode.
        Overlays image img2 on image img1. The overlay pixel combines
        multiply and screen: it multiplies dark pixels values and screen
        light values. Returns a composite image with the alpha channel
        retained.
        '''
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

        # Retain alpha channel from img1
        out_alpha = alpha1

        out = np.concatenate([out_rgb, out_alpha], axis=-1)
        out = np.clip(out * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(out, 'RGBA')

    def hue(self, img1, img2):
        '''Applies the hue blend mode.
        Hues image img1 with image img2. The hue filter replaces the
        hues of pixels in img1 with the hues of pixels in img2. Returns
        a composite image with the alpha channel retained.
        '''
        arr1 = np.array(img1).astype(np.float32) / 255.0
        arr2 = np.array(img2).astype(np.float32) / 255.0

        rgb1 = arr1[..., :3]
        rgb2 = arr2[..., :3]
        alpha1 = arr1[..., 3:4]

        shape = rgb1.shape
        flat_rgb1 = rgb1.reshape(-1, 3)
        flat_rgb2 = rgb2.reshape(-1, 3)

        out_rgb = np.zeros_like(flat_rgb1)
        for i in range(flat_rgb1.shape[0]):
            r1, g1, b1 = flat_rgb1[i]
            r2, g2, b2 = flat_rgb2[i]
            h1, l1, s1 = colorsys.rgb_to_hls(r1, g1, b1)
            h2, l2, s2 = colorsys.rgb_to_hls(r2, g2, b2)
            r, g, b = colorsys.hls_to_rgb(h2, l1, s1)
            out_rgb[i] = [r, g, b]

        out_rgb = out_rgb.reshape(shape)
        out = np.concatenate([out_rgb, alpha1], axis=-1)
        out = np.clip(out * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(out, 'RGBA')

    def color(self, img1, img2):
        '''Applies the color blend mode.
        Colorize image img1 with image img2. The color filter replaces
        the hue and saturation of pixels in img1 with the hue and
        saturation of pixels in img2. Returns a composite image with the
        alpha channel retained.
        '''
        arr1 = np.array(img1).astype(np.float32) / 255.0
        arr2 = np.array(img2).astype(np.float32) / 255.0

        rgb1 = arr1[..., :3]
        rgb2 = arr2[..., :3]
        alpha1 = arr1[..., 3:4]

        shape = rgb1.shape
        flat_rgb1 = rgb1.reshape(-1, 3)
        flat_rgb2 = rgb2.reshape(-1, 3)

        out_rgb = np.zeros_like(flat_rgb1)
        for i in range(flat_rgb1.shape[0]):
            r1, g1, b1 = flat_rgb1[i]
            r2, g2, b2 = flat_rgb2[i]
            h1, l1, s1 = colorsys.rgb_to_hls(r1, g1, b1)
            h2, l2, s2 = colorsys.rgb_to_hls(r2, g2, b2)
            r, g, b = colorsys.hls_to_rgb(h2, l1, s2)
            out_rgb[i] = [r, g, b]

        out_rgb = out_rgb.reshape(shape)
        out = np.concatenate([out_rgb, alpha1], axis=-1)
        out = np.clip(out * 255, 0, 255).astype(np.uint8)
        return Image.fromarray(out, 'RGBA')
