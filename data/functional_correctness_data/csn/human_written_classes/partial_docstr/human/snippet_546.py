class DisplayMixin:

    @property
    def visible(self):
        """
        Sets or returns whether the widget is visible.
        """
        return self._visible

    @visible.setter
    def visible(self, value):
        if value:
            self.show()
        else:
            self.hide()

    def hide(self):
        """Hide the widget."""
        self._visible = False
        self.master.display_widgets()

    def show(self):
        """Show the widget."""
        self._visible = True
        self.master.display_widgets()