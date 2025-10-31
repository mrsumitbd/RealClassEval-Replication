
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
        img1 = img1.convert('RGBA')
        img2 = img2.convert('RGBA')
        pixels1 = img1.load()
        pixels2 = img2.load()
        for x in range(img1.size[0]):
            for y in range(img1.size[1]):
                r1, g1, b1, a1 = pixels1[x, y]
                r2, g2, b2, a2 = pixels2[x, y]
                a = a1 + a2 - (a1 * a2 // 255)
                if a == 0:
                    pixels1[x, y] = (0, 0, 0, 0)
                else:
                    r = self._overlay_channel(r1, r2, a1, a2)
                    g = self._overlay_channel(g1, g2, a1, a2)
                    b = self._overlay_channel(b1, b2, a1, a2)
                    pixels1[x, y] = (r, g, b, a)
        return img1

    def _overlay_channel(self, c1, c2, a1, a2):
        c = (c1 * a1 + c2 * a2 - (c1 * c2 // 255) * a1 * a2 // 255) // (a1 +
                                                                        a2 - (a1 * a2 // 255)) if (a1 + a2 - (a1 * a2 // 255)) != 0 else 0
        if c2 <= 128:
            return int(2 * c1 * c2 / 255)
        else:
            return int(255 - 2 * (255 - c1) * (255 - c2) / 255)

    def hue(self, img1, img2):
        '''Applies the hue blend mode.
        Hues image img1 with image img2. The hue filter replaces the
        hues of pixels in img1 with the hues of pixels in img2. Returns
        a composite image with the alpha channel retained.
        '''
        img1 = img1.convert('RGBA')
        img2 = img2.convert('RGBA')
        pixels1 = img1.load()
        pixels2 = img2.load()
        for x in range(img1.size[0]):
            for y in range(img1.size[1]):
                r1, g1, b1, a1 = pixels1[x, y]
                r2, g2, b2, a2 = pixels2[x, y]
                a = a1 + a2 - (a1 * a2 // 255)
                if a == 0:
                    pixels1[x, y] = (0, 0, 0, 0)
                else:
                    h1, s1, v1 = self._rgb_to_hsv(r1, g1, b1)
                    h2, s2, v2 = self._rgb_to_hsv(r2, g2, b2)
                    r, g, b = self._hsv_to_rgb(h2, s1, v1)
                    r = int((r * a1 + r * a2) / (a1 + a2)
                            ) if (a1 + a2) != 0 else 0
                    g = int((g * a1 + g * a2) / (a1 + a2)
                            ) if (a1 + a2) != 0 else 0
                    b = int((b * a1 + b * a2) / (a1 + a2)
                            ) if (a1 + a2) != 0 else 0
                    pixels1[x, y] = (r, g, b, a)
        return img1

    def _rgb_to_hsv(self, r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0
        mx = max(r, g, b)
        mn = min(r, g, b)
        df = mx - mn
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        else:
            h = (60 * ((r - g) / df) + 240) % 360
        if mx == 0:
            s = 0
        else:
            s = df / mx
        v = mx
        return h, s, v

    def _hsv_to_rgb(self, h, s, v):
        h = h / 360.0
        i = int(h * 6.)
        f = h * 6. - i
        p = v * (1. - s)
        q = v * (1. - f * s)
        t = v * (1. - (1. - f) * s)
        i %= 6
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        else:
            r, g, b = v, p, q
        return int(r * 255), int(g * 255), int(b * 255)

    def color(self, img1, img2):
        '''Applies the color blend mode.
        Colorize image img1 with image img2. The color filter replaces
        the hue and saturation of pixels in img1 with the hue and
        saturation of pixels in img2. Returns a composite image with the
        alpha channel retained.
        '''
        img1 = img1.convert('RGBA')
        img2 = img2.convert('RGBA')
        pixels1 = img1.load()
        pixels2 = img2.load()
        for x in range(img1.size[0]):
            for y in range(img1.size[1]):
                r1, g1, b1, a1 = pixels1[x, y]
                r2, g2, b2, a2 = pixels2[x, y]
                a = a1 + a2 - (a1 * a2 // 255)
                if a == 0:
                    pixels1[x, y] = (0, 0, 0, 0)
                else:
                    h1, s1, v1 = self._rgb_to_hsv(r1, g1, b1)
                    h2, s2, v2 = self._rgb_to_hsv(r2, g2, b2)
                    r, g, b = self._hsv_to_rgb(h2, s2, v1)
                    r = int((r * a1 + r * a2) / (a1 + a2)
                            ) if (a1 + a2) != 0 else 0
                    g = int((g * a1 + g * a2) / (a1 + a2)
                            ) if (a1 + a2) != 0 else 0
                    b = int((b * a1 + b * a2) / (a1 + a2)
                            ) if (a1 + a2) != 0 else 0
                    pixels1[x, y] = (r, g, b, a)
        return img1
