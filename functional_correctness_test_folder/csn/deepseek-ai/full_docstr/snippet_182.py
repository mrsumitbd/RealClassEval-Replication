
import numpy as np
from PIL import Image


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
        if img1.mode != 'RGBA' or img2.mode != 'RGBA':
            raise ValueError("Images must be in RGBA mode.")

        arr1 = np.array(img1, dtype=np.float32) / 255.0
        arr2 = np.array(img2, dtype=np.float32) / 255.0

        alpha1 = arr1[:, :, 3]
        alpha2 = arr2[:, :, 3]

        rgb1 = arr1[:, :, :3]
        rgb2 = arr2[:, :, :3]

        mask = rgb1 <= 0.5
        result = np.where(mask, 2 * rgb1 * rgb2, 1 -
                          2 * (1 - rgb1) * (1 - rgb2))

        alpha = alpha1 + alpha2 * (1 - alpha1)
        result = np.dstack((result, alpha))
        result = (result * 255).clip(0, 255).astype(np.uint8)

        return Image.fromarray(result, 'RGBA')

    def hue(self, img1, img2):
        '''Applies the hue blend mode.
        Hues image img1 with image img2. The hue filter replaces the
        hues of pixels in img1 with the hues of pixels in img2. Returns
        a composite image with the alpha channel retained.
        '''
        if img1.mode != 'RGBA' or img2.mode != 'RGBA':
            raise ValueError("Images must be in RGBA mode.")

        arr1 = np.array(img1, dtype=np.float32) / 255.0
        arr2 = np.array(img2, dtype=np.float32) / 255.0

        alpha1 = arr1[:, :, 3]
        alpha2 = arr2[:, :, 3]

        hsv1 = np.array(img1.convert('HSV'), dtype=np.float32) / 255.0
        hsv2 = np.array(img2.convert('HSV'), dtype=np.float32) / 255.0

        hsv_result = np.dstack((hsv2[:, :, 0], hsv1[:, :, 1], hsv1[:, :, 2]))
        hsv_result = (hsv_result * 255).clip(0, 255).astype(np.uint8)

        rgb_result = Image.fromarray(hsv_result, 'HSV').convert('RGB')
        rgb_result = np.array(rgb_result, dtype=np.float32) / 255.0

        alpha = alpha1 + alpha2 * (1 - alpha1)
        result = np.dstack((rgb_result, alpha))
        result = (result * 255).clip(0, 255).astype(np.uint8)

        return Image.fromarray(result, 'RGBA')

    def color(self, img1, img2):
        '''Applies the color blend mode.
        Colorize image img1 with image img2. The color filter replaces
        the hue and saturation of pixels in img1 with the hue and
        saturation of pixels in img2. Returns a composite image with the
        alpha channel retained.
        '''
        if img1.mode != 'RGBA' or img2.mode != 'RGBA':
            raise ValueError("Images must be in RGBA mode.")

        arr1 = np.array(img1, dtype=np.float32) / 255.0
        arr2 = np.array(img2, dtype=np.float32) / 255.0

        alpha1 = arr1[:, :, 3]
        alpha2 = arr2[:, :, 3]

        hsv1 = np.array(img1.convert('HSV'), dtype=np.float32) / 255.0
        hsv2 = np.array(img2.convert('HSV'), dtype=np.float32) / 255.0

        hsv_result = np.dstack((hsv2[:, :, 0], hsv2[:, :, 1], hsv1[:, :, 2]))
        hsv_result = (hsv_result * 255).clip(0, 255).astype(np.uint8)

        rgb_result = Image.fromarray(hsv_result, 'HSV').convert('RGB')
        rgb_result = np.array(rgb_result, dtype=np.float32) / 255.0

        alpha = alpha1 + alpha2 * (1 - alpha1)
        result = np.dstack((rgb_result, alpha))
        result = (result * 255).clip(0, 255).astype(np.uint8)

        return Image.fromarray(result, 'RGBA')
