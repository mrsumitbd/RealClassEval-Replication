class Image:
    """
    Class to handle image stripe rendering.
    """

    def __init__(self, image):
        self._image = image

    def next_frame(self):
        self._frame = self._image.rendered_text

    def draw_stripe(self, screen, height, x, image_x):
        y_start, y_end = (0, height)
        if height > screen.height:
            y_start = (height - screen.height) // 2
            y_end = y_start + screen.height + 1
        for sy in range(y_start, y_end):
            try:
                y = int((screen.height - height) / 2) + sy
                image_y = int(sy * IMAGE_HEIGHT / height)
                char = self._frame[0][image_y][image_x]
                if char not in (' ', '.'):
                    fg, attr, bg = self._frame[1][image_y][image_x]
                    attr = 0 if attr is None else attr
                    bg = 0 if bg is None else bg
                    screen.print_at(char, x, y, fg, attr, bg)
            except IndexError:
                pass