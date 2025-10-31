
class Blend:

    def overlay(self, img1, img2):
        from PIL import Image, ImageEnhance
        img1 = img1.convert("RGBA")
        img2 = img2.convert("RGBA")
        blended = Image.blend(img1, img2, 0.5)
        return blended

    def hue(self, img1, img2):
        from PIL import Image, ImageEnhance
        img1 = img1.convert("HSV")
        img2 = img2.convert("HSV")
        img1_hue, img1_sat, img1_val = img1.split()
        img2_hue, img2_sat, img2_val = img2.split()
        blended_hue = Image.blend(img1_hue, img2_hue, 0.5)
        blended = Image.merge(
            "HSV", (blended_hue, img1_sat, img1_val)).convert("RGB")
        return blended

    def color(self, img1, img2):
        from PIL import Image, ImageEnhance
        img1 = img1.convert("RGB")
        img2 = img2.convert("RGB")
        img1_r, img1_g, img1_b = img1.split()
        img2_r, img2_g, img2_b = img2.split()
        blended_r = Image.blend(img1_r, img2_r, 0.5)
        blended_g = Image.blend(img1_g, img2_g, 0.5)
        blended_b = Image.blend(img1_b, img2_b, 0.5)
        blended = Image.merge("RGB", (blended_r, blended_g, blended_b))
        return blended
