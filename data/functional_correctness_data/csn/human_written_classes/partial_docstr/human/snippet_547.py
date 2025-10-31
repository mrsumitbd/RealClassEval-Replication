class EnableMixin:

    @property
    def enabled(self):
        state = self._get_tk_config('state')
        return state == 'normal' or state == 'active'

    @enabled.setter
    def enabled(self, value):
        if value:
            self.enable()
        else:
            self.disable()

    def disable(self):
        """Disable the widget."""
        self._set_tk_config('state', 'disabled')

    def enable(self):
        """Enable the widget."""
        self._set_tk_config('state', 'normal')