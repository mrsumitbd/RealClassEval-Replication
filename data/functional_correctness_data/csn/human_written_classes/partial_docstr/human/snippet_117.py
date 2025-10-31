class Sprite:
    """
    Dynamically sized sprite.
    """

    def __init__(self, state, x, y, images):
        self._state = state
        self.x, self.y = (x, y)
        self._images = images

    def next_frame(self):
        for image in self._images:
            image.next_frame()

    def draw_stripe(self, height, x, image_x):
        self._images[self._state.mode % 2].draw_stripe(self._state.screen, height, x, int(image_x * IMAGE_HEIGHT / height))