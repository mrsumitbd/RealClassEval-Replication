class ColorTextMixin:

    @property
    def text(self):
        return self.original_widget.text

    @text.setter
    def text(self, value):
        self.original_widget.set_text(value)

    def keypress(self, size, key):
        """ get rid of tback: `AttributeError: 'Text' object has no attribute 'keypress'` """
        return key