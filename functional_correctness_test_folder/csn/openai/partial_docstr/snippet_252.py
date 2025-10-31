class RGB888Format:
    '''RGB888Format'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        # Assume framebuf has attributes width and height and is a bytearray or mutable buffer
        width = getattr(framebuf, 'width', None)
        if width is None:
            raise AttributeError("framebuf must have a 'width' attribute")
        offset = (y * width + x) * 3
        framebuf[offset:offset+3] = bytes(color[:3])

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        width = getattr(framebuf, 'width', None)
        if width is None:
            raise AttributeError("framebuf must have a 'width' attribute")
        offset = (y * width + x) * 3
        return tuple(framebuf[offset:offset+3])

    @staticmethod
    def fill(framebuf, color):
        '''Fill the entire frame buffer with the given color.'''
        # color should be a sequence of 3 ints
        color_bytes = bytes(color[:3])
        # Use slice assignment for speed
        for i in range(0, len(framebuf), 3):
            framebuf[i:i+3] = color_bytes

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Fill a rectangle area with the given color.'''
        color_bytes = bytes(color[:3])
        buf_width = getattr(framebuf, 'width', None)
        if buf_width is None:
            raise AttributeError("framebuf must have a 'width' attribute")
        for row in range(y, y + height):
            base = (row * buf_width + x) * 3
            for col in range(width):
                offset = base + col * 3
                framebuf[offset:offset+3] = color_bytes
