
class MHMSBFormat:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buf']
        if not (0 <= x < width and 0 <= y < height):
            return
        byte_width = (width + 7) // 8
        byte_index = y * byte_width + (x // 8)
        bit = 7 - (x % 8)
        if color:
            buf[byte_index] |= (1 << bit)
        else:
            buf[byte_index] &= ~(1 << bit)

    @staticmethod
    def get_pixel(framebuf, x, y):
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buf']
        if not (0 <= x < width and 0 <= y < height):
            return 0
        byte_width = (width + 7) // 8
        byte_index = y * byte_width + (x // 8)
        bit = 7 - (x % 8)
        return (buf[byte_index] >> bit) & 1

    @staticmethod
    def fill(framebuf, color):
        width = framebuf['width']
        height = framebuf['height']
        buf = framebuf['buf']
        byte_width = (width + 7) // 8
        fill_byte = 0xFF if color else 0x00
        for y in range(height):
            for b in range(byte_width):
                buf[y * byte_width + b] = fill_byte
        # Mask out unused bits in last byte of each row if width is not multiple of 8
        if width % 8 != 0:
            mask = 0xFF << (8 - (width % 8))
            for y in range(height):
                idx = y * byte_width + (byte_width - 1)
                if color:
                    buf[idx] |= ~mask & 0xFF
                else:
                    buf[idx] &= mask

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        fb_width = framebuf['width']
        fb_height = framebuf['height']
        buf = framebuf['buf']
        byte_width = (fb_width + 7) // 8
        for j in range(y, y + height):
            if not (0 <= j < fb_height):
                continue
            for i in range(x, x + width):
                if not (0 <= i < fb_width):
                    continue
                MHMSBFormat.set_pixel(framebuf, i, j, color)
