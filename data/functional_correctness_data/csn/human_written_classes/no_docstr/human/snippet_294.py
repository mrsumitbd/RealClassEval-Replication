from functools import partial
from io import BytesIO
from PIL import Image, ImageChops, ImageFilter

class FrameAware:

    def __new__(cls, im):
        if getattr(im, 'n_frames', 1) > 1:
            return super().__new__(cls)
        return im

    def __init__(self, im):
        self.im = im

    def apply_to_frames(self, method, *args, **kwargs):
        new_frames = []
        for i in range(self.im.n_frames):
            self.im.seek(i)
            new_frames.append(method(*args, **kwargs))
        write_to = BytesIO()
        new_frames[0].save(write_to, format=self.im.format, save_all=True, append_images=new_frames[1:])
        return Image.open(write_to)

    def __getattr__(self, key):
        method = getattr(self.im, key)
        return partial(self.apply_to_frames, method)