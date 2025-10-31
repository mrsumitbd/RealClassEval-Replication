
from PIL import Image


class Blend:
    """
    A class used to blend two images using different techniques.

    Methods:
    -------
    overlay(img1, img2)
        Overlays img2 on top of img1.
    hue(img1, img2)
        Blends img1 and img2 using the hue blending mode.
    color(img1, img2)
        Blends img1 and img2 using the color blending mode.
    """

    def overlay(self, img1, img2):
        """
        Overlays img2 on top of img1.

        Parameters:
        ----------
        img1 : PIL.Image
            The base image.
        img2 : PIL.Image
            The image to be overlaid.

        Returns:
        -------
        PIL.Image
            The blended image.
        """
        img1 = img1.convert('RGBA')
        img2 = img2.convert('RGBA')
        blended_img = Image.blend(img1, img2, 0.5)
        return blended_img

    def hue(self, img1, img2):
        """
        Blends img1 and img2 using the hue blending mode.

        Parameters:
        ----------
        img1 : PIL.Image
            The base image.
        img2 : PIL.Image
            The image to be blended.

        Returns:
        -------
        PIL.Image
            The blended image.
        """
        img1 = img1.convert('RGB')
        img2 = img2.convert('RGB')
        img1_hsv = img1.convert('HSV')
        img2_hsv = img2.convert('HSV')
        blended_hsv = Image.merge(
            'HSV', (img2_hsv.split()[0], img1_hsv.split()[1], img1_hsv.split()[2]))
        blended_img = blended_hsv.convert('RGB')
        return blended_img

    def color(self, img1, img2):
        """
        Blends img1 and img2 using the color blending mode.

        Parameters:
        ----------
        img1 : PIL.Image
            The base image.
        img2 : PIL.Image
            The image to be blended.

        Returns:
        -------
        PIL.Image
            The blended image.
        """
        img1 = img1.convert('RGB')
        img2 = img2.convert('RGB')
        img1_hsv = img1.convert('HSV')
        img2_hsv = img2.convert('HSV')
        blended_hsv = Image.merge(
            'HSV', (img2_hsv.split()[0], img2_hsv.split()[1], img1_hsv.split()[2]))
        blended_img = blended_hsv.convert('RGB')
        return blended_img


# Example usage:
if __name__ == "__main__":
    img1 = Image.open('image1.jpg')
    img2 = Image.open('image2.jpg')

    blend = Blend()
    overlay_img = blend.overlay(img1, img2)
    hue_img = blend.hue(img1, img2)
    color_img = blend.color(img1, img2)

    overlay_img.save('overlay.jpg')
    hue_img.save('hue.jpg')
    color_img.save('color.jpg')
