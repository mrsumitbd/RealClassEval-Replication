class MVLSBFormat:
    '''MVLSBFormat'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        width = framebuf.width
        # Each byte holds 8 vertical pixels in a column
        byte_index = x + (y // 8) * width
        bit = 1 << (y % 8)  # LSB first
        if color:
            framebuf[byte_index] |= bit
        else:
            framebuf[byte_index] &= ~bit

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        width = framebuf.width
        byte_index = x + (y // 8) * width
        bit = 1 << (y % 8)
        return 1 if (framebuf[byte_index] & bit) else 0

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        fill_byte = 0xFF if color else 0x00
        for i in range(len(framebuf)):
            framebuf[i] = fill_byte

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        for yy in range(y, y + height):
            for xx in range(x, x + width):
                MVLSBFormat.set_pixel(framebuf, xx, yy, color)
