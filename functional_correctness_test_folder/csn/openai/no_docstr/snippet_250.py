
class MHMSBFormat:
    @staticmethod
    def _is_bytearray(buf):
        return isinstance(buf, (bytearray, memoryview))

    @staticmethod
    def _get_dimensions(buf):
        if hasattr(buf, "width") and hasattr(buf, "height"):
            return buf.width, buf.height
        if isinstance(buf, list) and buf:
            return len(buf[0]), len(buf)
        raise ValueError("Unsupported frame buffer format")

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        width, height = MHMSBFormat._get_dimensions(framebuf)
        if not (0 <= x < width and 0 <= y < height):
            return
        if MHMSBFormat._is_bytearray(framebuf):
            idx = (y * width + x) // 8
            bit = 7 - ((x % 8))
            if color:
                framebuf[idx] |= (1 << bit)
            else:
                framebuf[idx] &= ~(1 << bit)
        else:
            framebuf[y][x] = 1 if color else 0

    @staticmethod
    def get_pixel(framebuf, x, y):
        width, height = MHMSBFormat._get_dimensions(framebuf)
        if not (0 <= x < width and 0 <= y < height):
            return 0
        if MHMSBFormat._is_bytearray(framebuf):
            idx = (y * width + x) // 8
            bit = 7 - ((x % 8))
            return (framebuf[idx] >> bit) & 1
        else:
            return 1 if framebuf[y][x] else 0

    @staticmethod
    def fill(framebuf, color):
        width, height = MHMSBFormat._get_dimensions(framebuf)
        if MHMSBFormat._is_bytearray(framebuf):
            byte_val = 0xFF if color else 0x00
            framebuf[:] = bytearray([byte_val] * len(framebuf))
        else:
            for y in range(height):
                for x in range(width):
                    framebuf[y][x] = 1 if color else 0

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        buf_width, buf_height = MHMSBFormat._get_dimensions(framebuf)
        # Clamp rectangle to buffer bounds
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(buf_width, x + width)
        y1 = min(buf_height, y + height)
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                MHMSBFormat.set_pixel(framebuf, xx, yy, color)
