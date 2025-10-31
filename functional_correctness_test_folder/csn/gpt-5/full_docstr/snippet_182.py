from PIL import Image
import colorsys

try:
    import numpy as np
except Exception:
    np = None


class Blend:
    '''Layer blending modes.
    Implements additional blending modes to those present in PIL.
    These blending functions can not be used separately from
    the canvas.flatten() method, where the alpha compositing
    of two layers is handled.
    Since these blending are not part of a C library,
    but pure Python, they take forever to process.
    '''

    def _ensure_rgba(self, img):
        if img.mode != "RGBA":
            return img.convert("RGBA")
        return img

    def overlay(self, img1, img2):
        '''Applies the overlay blend mode.
        Overlays image img2 on image img1. The overlay pixel combines
        multiply and screen: it multiplies dark pixels values and screen
        light values. Returns a composite image with the alpha channel
        retained.
        '''
        img1 = self._ensure_rgba(img1)
        img2 = self._ensure_rgba(img2)

        if np is not None:
            a1 = np.array(img1)
            a2 = np.array(img2)
            base = a1[..., :3].astype(np.int16)
            blend = a2[..., :3].astype(np.int16)

            mask = base < 128
            out = np.empty_like(base)

            # result = (2*a*b)/255 when base<128
            out[mask] = (2 * base[mask] * blend[mask] + 255) // 255
            # result = 255 - 2*(255-a)*(255-b)/255 when base>=128
            inv_base = 255 - base[~mask]
            inv_blend = 255 - blend[~mask]
            out[~mask] = 255 - ((2 * inv_base * inv_blend + 255) // 255)

            out = np.clip(out, 0, 255).astype(np.uint8)
            # retain alpha from img1
            alpha = a1[..., 3:4]
            comp = np.concatenate([out, alpha], axis=2)
            return Image.fromarray(comp, mode="RGBA")

        # Fallback pure Python
        w, h = img1.size
        p1 = img1.load()
        p2 = img2.load()
        out = Image.new("RGBA", (w, h))
        po = out.load()

        for y in range(h):
            for x in range(w):
                r1, g1, b1, a = p1[x, y]
                r2, g2, b2, _ = p2[x, y]

                def ov(a_, b_):
                    if a_ < 128:
                        return (2 * a_ * b_) // 255
                    return 255 - ((2 * (255 - a_) * (255 - b_)) // 255)

                po[x, y] = (ov(r1, r2), ov(g1, g2), ov(b1, b2), a)
        return out

    def hue(self, img1, img2):
        '''Applies the hue blend mode.
        Hues image img1 with image img2. The hue filter replaces the
        hues of pixels in img1 with the hues of pixels in img2. Returns
        a composite image with the alpha channel retained.
        '''
        img1 = self._ensure_rgba(img1)
        img2 = self._ensure_rgba(img2)

        w, h = img1.size
        p1 = img1.load()
        p2 = img2.load()
        out = Image.new("RGBA", (w, h))
        po = out.load()

        for y in range(h):
            for x in range(w):
                r1, g1, b1, a1 = p1[x, y]
                r2, g2, b2, _ = p2[x, y]

                h1, l1, s1 = colorsys.rgb_to_hls(
                    r1 / 255.0, g1 / 255.0, b1 / 255.0)
                h2, l2, s2 = colorsys.rgb_to_hls(
                    r2 / 255.0, g2 / 255.0, b2 / 255.0)

                r, g, b = colorsys.hls_to_rgb(h2, l1, s1)
                po[x, y] = (int(round(r * 255)),
                            int(round(g * 255)), int(round(b * 255)), a1)
        return out

    def color(self, img1, img2):
        '''Applies the color blend mode.
        Colorize image img1 with image img2. The color filter replaces
        the hue and saturation of pixels in img1 with the hue and
        saturation of pixels in img2. Returns a composite image with the
        alpha channel retained.
        '''
        img1 = self._ensure_rgba(img1)
        img2 = self._ensure_rgba(img2)

        w, h = img1.size
        p1 = img1.load()
        p2 = img2.load()
        out = Image.new("RGBA", (w, h))
        po = out.load()

        for y in range(h):
            for x in range(w):
                r1, g1, b1, a1 = p1[x, y]
                r2, g2, b2, _ = p2[x, y]

                h1, l1, s1 = colorsys.rgb_to_hls(
                    r1 / 255.0, g1 / 255.0, b1 / 255.0)
                h2, l2, s2 = colorsys.rgb_to_hls(
                    r2 / 255.0, g2 / 255.0, b2 / 255.0)

                r, g, b = colorsys.hls_to_rgb(h2, l1, s2)
                po[x, y] = (int(round(r * 255)),
                            int(round(g * 255)), int(round(b * 255)), a1)
        return out
