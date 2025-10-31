
class RGB888Format:
    '''RGB888Format'''
    @staticmethod
    def set_pixel(framebuf, x, y, color):
        '''Set a given pixel to a color.'''
        if 0 <= x < len(framebuf[0]) and 0 <= y < len(framebuf):
            framebuf[y][x] = color

    @staticmethod
    def get_pixel(framebuf, x, y):
        '''Get the color of a given pixel'''
        if 0 <= x < len(framebuf[0]) and 0 <= y < len(framebuf):
            return framebuf[y][x]
        return 0

    @staticmethod
    def fill(framebuf, color):
        '''completely fill/clear the buffer with a color'''
        for row in framebuf:
            for i in range(len(row)):
                row[i] = color

    @staticmethod
    def fill_rect(framebuf, x, y, width, height, color):
        '''Draw a rectangle at the given location, size and color. The ``fill_rect`` method draws
        both the outline and interior.'''
        for dy in range(height):
            for dx in range(width):
                nx = x + dx
                ny = y + dy
                if 0 <= nx < len(framebuf[0]) and 0 <= ny < len(framebuf):
                    framebuf[ny][nx] = color
