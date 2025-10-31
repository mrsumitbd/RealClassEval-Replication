class Holder:
    """Helper class for holding configuration options"""

    def __init__(self):
        self.items = []

    def append_css(self, stylesheet):
        """Add extra css file name to component package"""
        self.items.append(stylesheet)

    def append_script(self, script):
        """Add extra script file name to component package"""
        self.items.append(script)