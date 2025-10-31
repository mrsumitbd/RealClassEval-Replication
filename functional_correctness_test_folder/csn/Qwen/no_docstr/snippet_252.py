
class RGB888Format:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        offset = (y * framebuf.width + x) * 3
        framebuf.buf[offset:offset+3] = color.to_bytes(3, 'big')

    @staticmethod
    def get_pixel(framebuf, x, y):
        offset = (y * framebuf.width + x) * 3
        return int.from_bytes(framebuf.buf[offset:offset+3], 'big')

    @staticmethod
    def fill(framebuf, color):
        framebuf.buf[:] = color.to_bytes(
            3, 'big') * (framebuf.width * framebuf.height)

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        color_bytes = color.to_bytes(3, 'big')
        for _y in range(y, y + height):
            offset = (_y * framebuf.width + x) * 3
            framebuf.buf[offset:offset + width * 3] = color_bytes * width
