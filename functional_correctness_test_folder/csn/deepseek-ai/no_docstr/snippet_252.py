
class RGB888Format:

    @staticmethod
    def set_pixel(framebuf, x, y, color):
        if x < 0 or y < 0 or x >= len(framebuf[0]) or y >= len(framebuf):
            return
        framebuf[y][x] = color

    @staticmethod
    def get_pixel(framebuf, x, y):
        if x < 0 or y < 0 or x >= len(framebuf[0]) or y >= len(framebuf):
            return None
        return framebuf[y][x]

    @staticmethod
    def fill(framebuf, color):
        for row in framebuf:
            for i in range(len(row)):
                row[i] = color

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        for dy in range(y, y + height):
            for dx in range(x, x + width):
                if 0 <= dx < len(framebuf[0]) and 0 <= dy < len(framebuf):
                    framebuf[dy][dx] = color
