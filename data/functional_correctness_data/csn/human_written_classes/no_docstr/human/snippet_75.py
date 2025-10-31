from guake.utils import HidePrevention

class MenuHideCallback:

    def __init__(self, window):
        self.window = window

    def on_hide(self, *args):
        HidePrevention(self.window).allow()