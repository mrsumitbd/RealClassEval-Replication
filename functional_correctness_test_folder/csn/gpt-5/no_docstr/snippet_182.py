import numpy as np
import colorsys


class Blend:
    def _to_float(self, img):
        img = np.asarray(img)
        if img.dtype == np.uint8:
            return img.astype(np.float32) / 255.0, ('uint8',)
        elif img.dtype == np.float32 or img.dtype == np.float64:
            return img.astype(np.float32), ('float', img.dtype)
        else:
            return img.astype(np.float32), ('float', np.float32)

    def _from_float(self, img_f, meta):
        img_f = np.clip(img_f, 0.0, 1.0)
        if meta[0] == 'uint8':
            return (img_f * 255.0 + 0.5).astype(np.uint8)
        else:
            return img_f.astype(meta[1])

    def _check_shapes(self, img1, img2):
        if img1.shape != img2.shape:
            raise ValueError("img1 and img2 must have the same shape")
        if img1.ndim != 3 or img1.shape[-1] not in (3, 4):
            raise ValueError("Images must have shape (H, W, 3) or (H, W, 4)")

    def overlay(self, img1, img2):
        self._check_shapes(img1, img2)
        f1, meta = self._to_float(img1)
        f2, _ = self._to_float(img2)

        has_alpha = f1.shape[-1] == 4
        if has_alpha:
            a = f1[..., 3:4]
            c1 = f1[..., :3]
            c2 = f2[..., :3]
        else:
            c1 = f1
            c2 = f2

        res = np.where(
            c1 <= 0.5,
            2.0 * c1 * c2,
            1.0 - 2.0 * (1.0 - c1) * (1.0 - c2)
        )
        res = np.clip(res, 0.0, 1.0)

        if has_alpha:
            out = np.concatenate([res, a], axis=-1)
        else:
            out = res
        return self._from_float(out, meta)

    def _apply_hls(self, img1, img2, mode):
        # mode: 'hue' (H from img2, L,S from img1) or 'color' (H,S from img2, L from img1)
        f1, meta = self._to_float(img1)
        f2, _ = self._to_float(img2)
        self._check_shapes(f1, f2)

        has_alpha = f1.shape[-1] == 4
        if has_alpha:
            a = f1[..., 3:4]
            c1 = f1[..., :3]
            c2 = f2[..., :3]
        else:
            c1 = f1
            c2 = f2

        H, W = c1.shape[:2]
        flat1 = c1.reshape(-1, 3)
        flat2 = c2.reshape(-1, 3)

        # Convert to HLS
        hls1 = np.empty_like(flat1)
        hls2 = np.empty_like(flat2)
        for i in range(flat1.shape[0]):
            r1, g1, b1 = flat1[i]
            r2, g2, b2 = flat2[i]
            h1, l1, s1 = colorsys.rgb_to_hls(r1, g1, b1)
            h2, l2, s2 = colorsys.rgb_to_hls(r2, g2, b2)
            if mode == 'hue':
                h, l, s = h2, l1, s1
            else:  # color
                h, l, s = h2, l1, s2
            r, g, b = colorsys.hls_to_rgb(h, l, s)
            hls1[i] = (r, g, b)

        res = hls1.reshape(H, W, 3)
        res = np.clip(res, 0.0, 1.0)

        if has_alpha:
            out = np.concatenate([res, a], axis=-1)
        else:
            out = res
        return self._from_float(out, meta)

    def hue(self, img1, img2):
        return self._apply_hls(img1, img2, mode='hue')

    def color(self, img1, img2):
        return self._apply_hls(img1, img2, mode='color')
