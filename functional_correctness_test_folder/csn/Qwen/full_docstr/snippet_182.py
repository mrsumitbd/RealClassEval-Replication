
from PIL import Image, ImageChops


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
        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")
        base, mask = img1.split()
        overlay, _ = img2.split()

        # Calculate the overlay
        overlay = ImageChops.multiply(base, overlay)
        screen = ImageChops.screen(base, overlay)

        # Determine which pixels to use
        mask = mask.point(lambda p: 255 if p > 128 else 0)
        result = Image.composite(screen, overlay, mask)

        # Merge with the original alpha
        result.putalpha(img1.split()[3])
        return result

    def hue(self, img1, img2):
        '''Applies the hue blend mode.
        Hues image img1 with image img2. The hue filter replaces the
        hues of pixels in img1 with the hues of pixels in img2. Returns
        a composite image with the alpha channel retained.
        '''
        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")

        h1, s1, l1 = img1.convert("HSV").split()
        h2, s2, l2 = img2.convert("HSV").split()

        # Replace hue of img1 with hue of img2
        result = Image.merge("HSV", (h2, s1, l1)).convert("RGBA")

        # Merge with the original alpha
        result.putalpha(img1.split()[3])
        return result

    def color(self, img1, img2):
        '''Applies the color blend mode.
        Colorize image img1 with image img2. The color filter replaces
        the hue and saturation of pixels in img1 with the hue and
        saturation of pixels in img2. Returns a composite image with the
        alpha channel retained.
        '''
        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")

        h1, s1, l1 = img1.convert("HSV").split()
        h2, s2, l2 = img2.convert("HSV").split()

        # Replace hue and saturation of img1 with hue and saturation of img2
        result = Image.merge("HSV", (h2, s2, l1)).convert("RGBA")

        # Merge with the original alpha
        result.putalpha(img1.split()[3])
        return result
