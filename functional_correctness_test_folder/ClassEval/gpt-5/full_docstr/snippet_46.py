from PIL import Image, ImageEnhance


class ImageProcessor:
    """
    This is a class to process image, including loading, saving, resizing, rotating, and adjusting the brightness of images.
    """

    def __init__(self):
        """
        Initialize self.image
        """
        self.image = None

    def _require_image(self):
        if self.image is None:
            raise ValueError("No image loaded. Call load_image() first.")

    def load_image(self, image_path):
        """
        Use Image util in PIL to open a image
        :param image_path: str, path of image that is to be
        >>> processor.load_image('test.jpg')
        >>> processor.image
        <PIL.JpegImagePlugin.JpegImageFile image mode=RGB size=3072x4096 at 0x194F2412A48>
        """
        if not isinstance(image_path, str):
            raise TypeError("image_path must be a string.")
        self.image = Image.open(image_path)
        return self.image

    def save_image(self, save_path):
        """
        Save image to a path if image has opened
        :param save_path: str, the path that the image will be saved
        >>> processor.load_image('test.jpg')
        >>> processor.save_image('test2.jpg')
        """
        self._require_image()
        if not isinstance(save_path, str):
            raise TypeError("save_path must be a string.")
        self.image.save(save_path)

    def resize_image(self, width, height):
        """
        Risize the image if image has opened.
        :param width: int, the target width of image
        :param height: int, the target height of image
        >>> processor.load_image('test.jpg')
        >>> processor.resize_image(300, 300)
        >>> processor.image.width
        300
        >>> processor.image.height
        300
        """
        self._require_image()
        if not isinstance(width, int) or not isinstance(height, int):
            raise TypeError("width and height must be integers.")
        if width <= 0 or height <= 0:
            raise ValueError("width and height must be positive.")
        self.image = self.image.resize((width, height), Image.LANCZOS)
        return self.image

    def rotate_image(self, degrees):
        """
        rotate image if image has opened
        :param degrees: float, the degrees that the image will be rotated
        >>> processor.load_image('test.jpg')
        >>> processor.resize_image(90)
        """
        self._require_image()
        if not isinstance(degrees, (int, float)):
            raise TypeError("degrees must be a number.")
        self.image = self.image.rotate(degrees, expand=True)
        return self.image

    def adjust_brightness(self, factor):
        """
        Adjust the brightness of image if image has opened.
        :param factor: float, brightness of an image. A factor of 0.0 gives a black image. A factor of 1.0 gives the original image.
        >>> processor.load_image('test.jpg')
        >>> processor.adjust_brightness(0.5)
        """
        self._require_image()
        if not isinstance(factor, (int, float)):
            raise TypeError("factor must be a number.")
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(factor)
        return self.image
