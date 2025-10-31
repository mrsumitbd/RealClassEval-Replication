import numpy as np
from PIL import Image


class Blend:

    def _to_rgba(self, img):
        if not isinstance(img, Image.Image):
            raise TypeError("img must be a PIL.Image")
        if img.mode != "RGBA":
            return img.convert("RGBA")
        return img

    def _overlay_rgb(self, base_rgb, blend_rgb):
        # base_rgb, blend_rgb: float32 arrays in [0,1], shape (H,W,3)
        low_mask = base_rgb <= 0.5
        high_mask = ~low_mask
        out = np.empty_like(base_rgb)
        out[low_mask] = 2.0 * base_rgb[low_mask] * blend_rgb[low_mask]
        out[high_mask] = 1.0 - 2.0 * \
            (1.0 - base_rgb[high_mask]) * (1.0 - blend_rgb[high_mask])
        return np.clip(out, 0.0, 1.0)

    def _rgb_to_hls(self, rgb):
        # rgb: float array [0,1], shape (...,3)
        r = rgb[..., 0]
        g = rgb[..., 1]
        b = rgb[..., 2]
        maxc = np.maximum(np.maximum(r, g), b)
        minc = np.minimum(np.minimum(r, g), b)
        l = (minc + maxc) / 2.0

        h = np.zeros_like(l)
        s = np.zeros_like(l)

        diff = maxc - minc
        non_zero = diff > 1e-12

        # Saturation
        s_tmp = np.empty_like(s)
        # where l <= 0.5
        mask_low_l = (l <= 0.5) & non_zero
        mask_high_l = (l > 0.5) & non_zero
        s_tmp[mask_low_l] = diff[mask_low_l] / \
            (maxc[mask_low_l] + minc[mask_low_l])
        s_tmp[mask_high_l] = diff[mask_high_l] / \
            (2.0 - maxc[mask_high_l] - minc[mask_high_l])
        s[non_zero] = s_tmp[non_zero]
        s[~non_zero] = 0.0

        # Hue
        rc = np.zeros_like(r)
        gc = np.zeros_like(g)
        bc = np.zeros_like(b)
        rc[non_zero] = (maxc - r)[non_zero] / diff[non_zero]
        gc[non_zero] = (maxc - g)[non_zero] / diff[non_zero]
        bc[non_zero] = (maxc - b)[non_zero] / diff[non_zero]

        is_r = (r == maxc) & non_zero
        is_g = (g == maxc) & non_zero
        is_b = (b == maxc) & non_zero

        h[is_r] = (bc - gc)[is_r]
        h[is_g] = 2.0 + (rc - bc)[is_g]
        h[is_b] = 4.0 + (gc - rc)[is_b]

        h = (h / 6.0) % 1.0
        h[~non_zero] = 0.0

        return np.stack([h, l, s], axis=-1)

    def _hls_to_rgb(self, hls):
        # hls: float array [0,1], shape (...,3)
        h = hls[..., 0]
        l = hls[..., 1]
        s = hls[..., 2]

        r = np.empty_like(h)
        g = np.empty_like(h)
        b = np.empty_like(h)

        def hue_to_rgb(m1, m2, hval):
            hval = hval % 1.0
            out = np.empty_like(hval)
            cond1 = hval < (1.0 / 6.0)
            cond2 = (hval >= (1.0 / 6.0)) & (hval < 0.5)
            cond3 = (hval >= 0.5) & (hval < (2.0 / 3.0))
            out[cond1] = m1[cond1] + \
                (m2[cond1] - m1[cond1]) * 6.0 * hval[cond1]
            out[cond2] = m2[cond2]
            out[cond3] = m1[cond3] + \
                (m2[cond3] - m1[cond3]) * (2.0 / 3.0 - hval[cond3]) * 6.0
            mask_else = ~(cond1 | cond2 | cond3)
            out[mask_else] = m1[mask_else]
            return out

        # If s == 0 then r=g=b=l
        no_sat = s <= 1e-12
        sat = ~no_sat

        r[no_sat] = l[no_sat]
        g[no_sat] = l[no_sat]
        b[no_sat] = l[no_sat]

        if np.any(sat):
            l_sat = l[sat]
            s_sat = s[sat]
            h_sat = h[sat]
            m2 = np.empty_like(l_sat)
            low_mask = l_sat <= 0.5
            m2[low_mask] = l_sat[low_mask] * (1.0 + s_sat[low_mask])
            m2[~low_mask] = l_sat[~low_mask] + s_sat[~low_mask] - \
                l_sat[~low_mask] * s_sat[~low_mask]
            m1 = 2.0 * l_sat - m2

            r_sat = hue_to_rgb(m1, m2, h_sat + 1.0 / 3.0)
            g_sat = hue_to_rgb(m1, m2, h_sat)
            b_sat = hue_to_rgb(m1, m2, h_sat - 1.0 / 3.0)

            r[sat] = r_sat
            g[sat] = g_sat
            b[sat] = b_sat

        rgb = np.stack([r, g, b], axis=-1)
        return np.clip(rgb, 0.0, 1.0)

    def overlay(self, img1, img2):
        '''Applies the overlay blend mode.
        Overlays image img2 on image img1. The overlay pixel combines
        multiply and screen: it multiplies dark pixels values and screen
        light values. Returns a composite image with the alpha channel
        retained.
        '''
        base = self._to_rgba(img1)
        blend = self._to_rgba(img2)
        if base.size != blend.size:
            raise ValueError("Images must be the same size")

        base_arr = np.asarray(base, dtype=np.uint8)
        blend_arr = np.asarray(blend, dtype=np.uint8)

        base_rgb = base_arr[..., :3].astype(np.float32) / 255.0
        blend_rgb = blend_arr[..., :3].astype(np.float32) / 255.0

        out_rgb = self._overlay_rgb(base_rgb, blend_rgb)
        out_rgb_u8 = (out_rgb * 255.0 + 0.5).astype(np.uint8)

        out_a = base_arr[..., 3:4]  # retain alpha from base
        out = np.concatenate([out_rgb_u8, out_a], axis=-1)
        return Image.fromarray(out, mode="RGBA")

    def hue(self, img1, img2):
        '''Applies the hue blend mode.
        Hues image img1 with image img2. The hue filter replaces the
        hues of pixels in img1 with the hues of pixels in img2. Returns
        a composite image with the alpha channel retained.
        '''
        base = self._to_rgba(img1)
        blend = self._to_rgba(img2)
        if base.size != blend.size:
            raise ValueError("Images must be the same size")

        base_arr = np.asarray(base, dtype=np.uint8)
        blend_arr = np.asarray(blend, dtype=np.uint8)

        base_rgb = base_arr[..., :3].astype(np.float32) / 255.0
        blend_rgb = blend_arr[..., :3].astype(np.float32) / 255.0

        base_hls = self._rgb_to_hls(base_rgb)
        blend_hls = self._rgb_to_hls(blend_rgb)

        out_hls = base_hls.copy()
        # take hue from blend; keep L and S from base
        out_hls[..., 0] = blend_hls[..., 0]

        out_rgb = self._hls_to_rgb(out_hls)
        out_rgb_u8 = (out_rgb * 255.0 + 0.5).astype(np.uint8)

        out_a = base_arr[..., 3:4]
        out = np.concatenate([out_rgb_u8, out_a], axis=-1)
        return Image.fromarray(out, mode="RGBA")

    def color(self, img1, img2):
        base = self._to_rgba(img1)
        blend = self._to_rgba(img2)
        if base.size != blend.size:
            raise ValueError("Images must be the same size")

        base_arr = np.asarray(base, dtype=np.uint8)
        blend_arr = np.asarray(blend, dtype=np.uint8)

        base_rgb = base_arr[..., :3].astype(np.float32) / 255.0
        blend_rgb = blend_arr[..., :3].astype(np.float32) / 255.0

        base_hls = self._rgb_to_hls(base_rgb)
        blend_hls = self._rgb_to_hls(blend_rgb)

        out_hls = np.empty_like(base_hls)
        # color blend: hue and saturation from blend, luminance (lightness) from base
        out_hls[..., 0] = blend_hls[..., 0]
        out_hls[..., 2] = blend_hls[..., 2]
        out_hls[..., 1] = base_hls[..., 1]

        out_rgb = self._hls_to_rgb(out_hls)
        out_rgb_u8 = (out_rgb * 255.0 + 0.5).astype(np.uint8)

        out_a = base_arr[..., 3:4]
        out = np.concatenate([out_rgb_u8, out_a], axis=-1)
        return Image.fromarray(out, mode="RGBA")
