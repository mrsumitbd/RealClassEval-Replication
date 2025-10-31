
from PIL import Image
import numpy as np
import colorsys


class Blend:

    def overlay(self, img1, img2):
        '''Applies the overlay blend mode.
        Overlays image img2 on image img1. The overlay pixel combines
        multiply and screen: it multiplies dark pixels values and screen
        light values. Returns a composite image with the alpha channel
        retained.
        '''
        img1 = img1.convert('RGBA')
        img2 = img2.convert('RGBA')

        img1_array = np.array(img1)
        img2_array = np.array(img2)

        # Normalize pixel values to be between 0 and 1
        img1_array = img1_array / 255.0
        img2_array = img2_array / 255.0

        # Apply overlay blend mode
        composite = np.copy(img1_array)
        for i in range(3):  # RGB channels
            composite[:, :, i] = np.where(img1_array[:, :, i] < 0.5,
                                          2 * img1_array[:, :, i] *
                                          img2_array[:, :, i],
                                          1 - 2 * (1 - img1_array[:, :, i]) * (1 - img2_array[:, :, i]))

        # Retain alpha channel from img1
        composite[:, :, 3] = img1_array[:, :, 3]

        # Convert back to uint8 and create Image object
        composite = (composite * 255).astype(np.uint8)
        return Image.fromarray(composite)

    def hue(self, img1, img2):
        '''Applies the hue blend mode.
        Hues image img1 with image img2. The hue filter replaces the
        hues of pixels in img1 with the hues of pixels in img2. Returns
        a composite image with the alpha channel retained.
        '''
        img1 = img1.convert('RGBA')
        img2 = img2.convert('RGBA')

        img1_array = np.array(img1)
        img2_array = np.array(img2)

        # Normalize pixel values to be between 0 and 1
        img1_array = img1_array / 255.0
        img2_array = img2_array / 255.0

        # Apply hue blend mode
        composite = np.copy(img1_array)
        height, width, _ = img1_array.shape
        for y in range(height):
            for x in range(width):
                if img2_array[y, x, 3] > 0:  # Check if pixel is not fully transparent
                    # Convert to HSV
                    h1, s1, v1 = colorsys.rgb_to_hsv(
                        img1_array[y, x, 0], img1_array[y, x, 1], img1_array[y, x, 2])
                    h2, _, _ = colorsys.rgb_to_hsv(
                        img2_array[y, x, 0], img2_array[y, x, 1], img2_array[y, x, 2])

                    # Replace hue with hue from img2
                    r, g, b = colorsys.hsv_to_rgb(h2, s1, v1)

                    composite[y, x, 0] = r
                    composite[y, x, 1] = g
                    composite[y, x, 2] = b

        # Retain alpha channel from img1
        composite[:, :, 3] = img1_array[:, :, 3]

        # Convert back to uint8 and create Image object
        composite = (composite * 255).astype(np.uint8)
        return Image.fromarray(composite)

    def color(self, img1, img2):
        '''Applies the color blend mode.
        Colors image img1 with image img2. The color filter replaces the
        color (hue and saturation) of pixels in img1 with the color of
        pixels in img2, while retaining the luminance of img1. Returns
        a composite image with the alpha channel retained.
        '''
        img1 = img1.convert('RGBA')
        img2 = img2.convert('RGBA')

        img1_array = np.array(img1)
        img2_array = np.array(img2)

        # Normalize pixel values to be between 0 and 1
        img1_array = img1_array / 255.0
        img2_array = img2_array / 255.0

        # Apply color blend mode
        composite = np.copy(img1_array)
        height, width, _ = img1_array.shape
        for y in range(height):
            for x in range(width):
                if img2_array[y, x, 3] > 0:  # Check if pixel is not fully transparent
                    # Convert to HSL (using colorsys which uses HSV, so we need to adjust)
                    r1, g1, b1 = img1_array[y, x, :3]
                    h1, s1, v1 = colorsys.rgb_to_hsv(r1, g1, b1)
                    l1 = v1 - (s1 * v1 / 2)  # Approximating luminance

                    r2, g2, b2 = img2_array[y, x, :3]
                    h2, s2, _ = colorsys.rgb_to_hsv(r2, g2, b2)

                    # Replace hue and saturation with values from img2, retain luminance
                    s = s2
                    h = h2

                    # Convert back to RGB
                    # Adjusting value to retain luminance
                    r, g, b = colorsys.hsv_to_rgb(h, s, l1 + (s * l1))

                    composite[y, x, 0] = r
                    composite[y, x, 1] = g
                    composite[y, x, 2] = b

        # Retain alpha channel from img1
        composite[:, :, 3] = img1_array[:, :, 3]

        # Convert back to uint8 and create Image object
        composite = (composite * 255).astype(np.uint8)
        return Image.fromarray(composite)
