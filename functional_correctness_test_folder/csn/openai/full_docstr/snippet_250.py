
class MHMSBFormat:
    '''MHMSBFormat'''

    @staticmethod
    def _index(framebuf, x, y):
        """Return the byte index and bit mask for the pixel at (x, y)."""
        width = framebuf['width']
        # linear pixel index
        idx = y * width + x
        byte_index = idx >> 3          # idx // 8
        bit_index = 7 - (idx & 7)      # MSB first
        mask = 1 << bit_index
        return byte_index, mask

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        byte_index, mask = MHMSBFormat._index(framebuf, x, y)
        if color:
            framebuf['data'][byte_index] |= mask
        else:
            framebuf['data'][byte_index] &= ~mask

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        byte_index, mask = MHMSBFormat._index(framebuf, x, y)
        return 1 if (framebuf['data'][byte_index] & mask) else 0

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        byte_val = 0xFF if color else 0x00
        framebuf['data'][:] = bytearray([byte_val] * len(framebuf['data']))

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        for yy in range(y, y + height):
            for xx in range(x, x + width):
                MHMSBFormat.set_pixel(framebuf, xx, yy, color)
