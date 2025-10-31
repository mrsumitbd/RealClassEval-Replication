
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
        width, height = img1.size
        composite = img1.copy()

        for x in range(width):
            for y in range(height):
                r1, g1, b1, a1 = img1.getpixel((x, y))
                r2, g2, b2, a2 = img2.getpixel((x, y))

                if r1 < 128:
                    r = 2 * r1 * r2 / 255
                else:
                    r = 255 - 2 * (255 - r1) * (255 - r2) / 255

                if g1 < 128:
                    g = 2 * g1 * g2 / 255
                else:
                    g = 255 - 2 * (255 - g1) * (255 - g2) / 255

                if b1 < 128:
                    b = 2 * b1 * b2 / 255
                else:
                    b = 255 - 2 * (255 - b1) * (255 - b2) / 255

                composite.putpixel((x, y), (int(r), int(g), int(b), a1))

        return composite

    def hue(self, img1, img2):
        '''Applies the hue blend mode.
        Hues image img1 with image img2. The hue filter replaces the
        hues of pixels in img1 with the hues of pixels in img2. Returns
        a composite image with the alpha channel retained.
        '''
        img1 = img1.convert('RGBA')
        img2 = img2.convert('RGBA')
        width, height = img1.size
        composite = img1.copy()

        for x in range(width):
            for y in range(height):
                r1, g1, b1, a1 = img1.getpixel((x, y))
                r2, g2, b2, a2 = img2.getpixel((x, y))

                h1, s1, v1 = self.rgb_to_hsv(r1, g1, b1)
                h2, s2, v2 = self.rgb_to_hsv(r2, g2, b2)

                r, g, b = self.hsv_to_rgb(h2, s1, v1)
                composite.putpixel((x, y), (int(r), int(g), int(b), a1))

        return composite

    def color(self, img1, img2):
        '''Applies the color blend mode.
        Colorize image img1 with image img2. The color filter replaces
        the hue and saturation of pixels in img1 with the hue and
        saturation of pixels in img2. Returns a composite image with the
        alpha channel retained.
        '''
        img1 = img1.convert('RGBA')
        img2 = img2.convert('RGBA')
        width, height = img1.size
        composite = img1.copy()

        for x in range(width):
            for y in range(height):
                r1, g1, b1, a1 = img1.getpixel((x, y))
                r2, g2, b2, a2 = img2.getpixel((x, y))

                h1, s1, v1 = self.rgb_to_hsv(r1, g1, b1)
                h2, s2, v2 = self.rgb_to_hsv(r2, g2, b2)

                r, g, b = self.hsv_to_rgb(h2, s2, v1)
                composite.putpixel((x, y), (int(r), int(g), int(b), a1))

        return composite

    def rgb_to_hsv(self, r, g, b):
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
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360

        if mx == 0:
            s = 0
        else:
            s = (df / mx) * 100

        v = mx * 100
        return h, s, v

    def hsv_to_rgb(self, h, s, v):
        s /= 100
        v /= 100
        C = s * v
        X = C * (1 - abs((h / 60) % 2 - 1))
        m = v - C
        h %= 360

        if h < 60:
            r, g, b = C, X, 0
        elif h < 120:
            r, g, b = X, C, 0
        elif h < 180:
            r, g, b = 0, C, X
        elif h < 240:
            r, g, b = 0, X, C
        elif h < 300:
            r, g, b = X, 0, C
        else:
            r, g, b = C, 0, X

        r = (r + m) * 255
        g = (g + m) * 255
        b = (b + m) * 255
        return r, g, b
