
import colorsys
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
        if img1.size != img2.size:
            raise ValueError("Images must be the same size")
        # Ensure both images are in RGBA
        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")
        w, h = img1.size
        out = Image.new("RGBA", (w, h))
        pix1 = img1.load()
        pix2 = img2.load()
        outpix = out.load()
        for y in range(h):
            for x in range(w):
                r1, g1, b1, a1 = pix1[x, y]
                r2, g2, b2, a2 = pix2[x, y]
                # Overlay for each channel

                def overlay_ch(c1, c2):
                    if c2 < 128:
                        return (2 * c1 * c2) // 255
                    else:
                        return 255 - (2 * (255 - c1) * (255 - c2)) // 255
                r = overlay_ch(r1, r2)
                g = overlay_ch(g1, g2)
                b = overlay_ch(b1, b2)
                outpix[x, y] = (r, g, b, a1)  # keep alpha from img1
        return out

    def hue(self, img1, img2):
        '''Applies the hue blend mode.
        Hues image img1 with image img2. The hue filter replaces the
        hues of pixels in img1 with the hues of pixels in img2. Returns
        a composite image with the alpha channel retained.
        '''
        if img1.size != img2.size:
            raise ValueError("Images must be the same size")
        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")
        w, h = img1.size
        out = Image.new("RGBA", (w, h))
        pix1 = img1.load()
        pix2 = img2.load()
        outpix = out.load()
        for y in range(h):
            for x in range(w):
                r1, g1, b1, a1 = pix1[x, y]
                r2, g2, b2, a2 = pix2[x, y]
                # Convert to HSV
                h1, s1, v1 = colorsys.rgb_to_hsv(
                    r1 / 255.0, g1 / 255.0, b1 / 255.0)
                h2, s2, v2 = colorsys.rgb_to_hsv(
                    r2 / 255.0, g2 / 255.0, b2 / 255.0)
                # Replace hue of img1 with hue of img2
                h_new = h2
                r, g, b = colorsys.hsv_to_rgb(h_new, s1, v1)
                outpix[x, y] = (int(r * 255), int(g * 255), int(b * 255), a1)
        return out

    def color(self, img1, img2):
        '''Applies the color blend mode.
        Colorize image img1 with image img2. The color filter replaces the hue and saturation of pixels in img1 with the hue and saturation of pixels in img2. Returns a composite image with the alpha channel retained.
        '''
        if img1.size != img2.size:
            raise ValueError("Images must be the same size")
        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")
        w, h = img1.size
        out = Image.new("RGBA", (w, h))
        pix1 = img1.load()
        pix2 = img2.load()
        outpix = out.load()
        for y in range(h):
            for x in range(w):
                r1, g1, b1, a1 = pix1[x, y]
                r2, g2, b2, a2 = pix2[x, y]
                # Convert to HSV
                h1, s1, v1 = colorsys.rgb_to_hsv(
                    r1 / 255.0, g1 / 255.0, b1 / 255.0)
                h2, s2, v2 = colorsys.rgb_to_hsv(
                    r2 / 255.0, g2 / 255.0, b2 / 255.0)
                # Replace hue and saturation of img1 with those of img2
                r, g, b = colorsys.hsv_to_rgb(h2, s2, v1)
                outpix[x, y] = (int(r * 255), int(g * 255), int(b * 255), a1)
        return out
