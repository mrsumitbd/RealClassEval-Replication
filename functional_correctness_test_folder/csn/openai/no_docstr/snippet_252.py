
class RGB888Format:
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        """
        Set the pixel at (x, y) to the given RGB888 color.

        Parameters
        ----------
        framebuf : bytearray or memoryview
            The frame buffer containing the image data. It must have
            attributes `width` and `height` that specify the image
            dimensions.
        x, y : int
            The coordinates of the pixel to set.
        color : tuple or list of 3 ints
            The RGB888 color to write. Each component must be in the
            range 0–255.
        """
        width = getattr(framebuf, "width", None)
        height = getattr(framebuf, "height", None)
        if width is None or height is None:
            raise AttributeError(
                "framebuf must have 'width' and 'height' attributes")

        if not (0 <= x < width and 0 <= y < height):
            raise ValueError("pixel coordinates out of bounds")

        idx = (y * width + x) * 3
        framebuf[idx] = color[0]
        framebuf[idx + 1] = color[1]
        framebuf[idx + 2] = color[2]

    @staticmethod
    def get_pixel(framebuf, x, y):
        """
        Retrieve the RGB888 color of the pixel at (x, y).

        Parameters
        ----------
        framebuf : bytearray or memoryview
            The frame buffer containing the image data. It must have
            attributes `width` and `height` that specify the image
            dimensions.
        x, y : int
            The coordinates of the pixel to read.

        Returns
        -------
        tuple
            The RGB888 color as a tuple of three integers.
        """
        width = getattr(framebuf, "width", None)
        height = getattr(framebuf, "height", None)
        if width is None or height is None:
            raise AttributeError(
                "framebuf must have 'width' and 'height' attributes")

        if not (0 <= x < width and 0 <= y < height):
            raise ValueError("pixel coordinates out of bounds")

        idx = (y * width + x) * 3
        return (framebuf[idx], framebuf[idx + 1], framebuf[idx + 2])

    @staticmethod
    def fill(framebuf, color):
        """
        Fill the entire frame buffer with the given RGB888 color.

        Parameters
        ----------
        framebuf : bytearray or memoryview
            The frame buffer containing the image data. It must have
            attributes `width` and `height` that specify the image
            dimensions.
        color : tuple or list of 3 ints
            The RGB888 color to use for filling.
        """
        width = getattr(framebuf, "width", None)
        height = getattr(framebuf, "height", None)
        if width is None or height is None:
            raise AttributeError(
                "framebuf must have 'width' and 'height' attributes")

        r, g, b = color
        pixel_bytes = bytes((r, g, b))
        # Repeat the pixel bytes for the entire buffer
        framebuf[:] = pixel_bytes * (width * height)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        """
        Fill a rectangular region of the frame buffer with the given RGB888 color.

        Parameters
        ----------
        framebuf : bytearray or memoryview
            The frame buffer containing the image data. It must have
            attributes `width` and `height` that specify the image
            dimensions.
        x, y : int
            The top-left corner of the rectangle.
        width, height : int
            The dimensions of the rectangle.
        color : tuple or list of 3 ints
            The RGB888 color to use for filling.
        """
        buf_width = getattr(framebuf, "width", None)
        buf_height = getattr(framebuf, "height", None)
        if buf_width is None or buf_height is None:
            raise AttributeError(
                "framebuf must have 'width' and 'height' attributes")

        if x < 0 or y < 0 or x + width > buf_width or y + height > buf_height:
            raise ValueError("rectangle out of bounds")

        r, g, b = color
        for row in range(y, y + height):
            base = (row * buf_width + x) * 3
            for col in range(width):
                idx = base + col * 3
                framebuf[idx] = r
                framebuf[idx + 1] = g
                framebuf[idx + 2] = b
