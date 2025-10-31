import numpy as np
from ultralytics.utils.checks import check_requirements

class LoadScreenshots:
    """
    Ultralytics screenshot dataloader for capturing and processing screen images.

    This class manages the loading of screenshot images for processing with YOLO. It is suitable for use with
    `yolo predict source=screen`.

    Attributes:
        source (str): The source input indicating which screen to capture.
        screen (int): The screen number to capture.
        left (int): The left coordinate for screen capture area.
        top (int): The top coordinate for screen capture area.
        width (int): The width of the screen capture area.
        height (int): The height of the screen capture area.
        mode (str): Set to 'stream' indicating real-time capture.
        frame (int): Counter for captured frames.
        sct (mss.mss): Screen capture object from `mss` library.
        bs (int): Batch size, set to 1.
        fps (int): Frames per second, set to 30.
        monitor (Dict[str, int]): Monitor configuration details.

    Methods:
        __iter__: Returns an iterator object.
        __next__: Captures the next screenshot and returns it.

    Examples:
        >>> loader = LoadScreenshots("0 100 100 640 480")  # screen 0, top-left (100,100), 640x480
        >>> for source, im, im0s, vid_cap, s in loader:
        ...     print(f"Captured frame: {im.shape}")
    """

    def __init__(self, source):
        """Initialize screenshot capture with specified screen and region parameters."""
        check_requirements('mss')
        import mss
        source, *params = source.split()
        self.screen, left, top, width, height = (0, None, None, None, None)
        if len(params) == 1:
            self.screen = int(params[0])
        elif len(params) == 4:
            left, top, width, height = (int(x) for x in params)
        elif len(params) == 5:
            self.screen, left, top, width, height = (int(x) for x in params)
        self.mode = 'stream'
        self.frame = 0
        self.sct = mss.mss()
        self.bs = 1
        self.fps = 30
        monitor = self.sct.monitors[self.screen]
        self.top = monitor['top'] if top is None else monitor['top'] + top
        self.left = monitor['left'] if left is None else monitor['left'] + left
        self.width = width or monitor['width']
        self.height = height or monitor['height']
        self.monitor = {'left': self.left, 'top': self.top, 'width': self.width, 'height': self.height}

    def __iter__(self):
        """Yields the next screenshot image from the specified screen or region for processing."""
        return self

    def __next__(self):
        """Captures and returns the next screenshot as a numpy array using the mss library."""
        im0 = np.asarray(self.sct.grab(self.monitor))[:, :, :3]
        s = f'screen {self.screen} (LTWH): {self.left},{self.top},{self.width},{self.height}: '
        self.frame += 1
        return ([str(self.screen)], [im0], [s])