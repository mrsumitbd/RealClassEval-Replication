from gi.repository import Gtk

class HidePrevention:

    def __init__(self, window):
        """Create a new HidePrevention object like `HidePrevention(window)`"""
        if not isinstance(window, Gtk.Window):
            raise ValueError(f'window must be of type Gtk.Window, not of type {type(window)}')
        self.window = window

    def may_hide(self):
        """returns True if the window is allowed to hide and
        False if `prevent()` is called from some where
        """
        return getattr(self.window, 'can_hide', True)

    def prevent(self):
        """sets a flag on the window object which indicates to
        may_hide that the window is NOT allowed to be hidden.
        """
        setattr(self.window, 'can_hide', False)

    def allow(self):
        """sets the flag so that it indicates to may_hide that the window is allowed to be hidden"""
        setattr(self.window, 'can_hide', True)