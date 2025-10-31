
from PIL import Image, ImageChops


class Blend:

    def overlay(self, img1, img2):
        '''Applies the overlay blend mode.
        Overlays image img2 on image img1. The overlay pixel combines
        multiply and screen: it multiplies dark pixels values and screen
        light values. Returns a composite image with the alpha channel
        retained.
        '''
        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")

        def overlay_channel(c1, c2):
            return c1 * c2 / 255 if c1 < 128 else 255 - (255 - c1) * (255 - c2) / 255

        r1, g1, b1, a1 = img1.split()
        r2, g2, b2, a2 = img2.split()

        r1, g1, b1 = r1.point(
            lambda p: p / 255.0), g1.point(lambda p: p / 255.0), b1.point(lambda p: p / 255.0)
        r2, g2, b2 = r2.point(
            lambda p: p / 255.0), g2.point(lambda p: p / 255.0), b2.point(lambda p: p / 255.0)

        r = ImageChops.add(ImageChops.multiply(r1, r2), ImageChops.multiply(
            ImageChops.invert(r1), ImageChops.invert(r2)), scale=255)
        g = ImageChops.add(ImageChops.multiply(g1, g2), ImageChops.multiply(
            ImageChops.invert(g1), ImageChops.invert(g2)), scale=255)
        b = ImageChops.add(ImageChops.multiply(b1, b2), ImageChops.multiply(
            ImageChops.invert(b1), ImageChops.invert(b2)), scale=255)

        return Image.merge("RGBA", (r, g, b, a1))

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

        return Image.merge("HSV", (h2, s1, l1)).convert("RGBA")

    def color(self, img1, img2):
        '''Applies the color blend mode.
        Colors image img1 with image img2. The color filter replaces the
        colors of pixels in img1 with the colors of pixels in img2. Returns
        a composite image with the alpha channel retained.
        '''
        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")

        h1, s1, l1 = img1.convert("HSV").split()
        h2, s2, l2 = img2.convert("HSV").split()

        return Image.merge("HSV", (h2, s2, l1)).convert("RGBA")
