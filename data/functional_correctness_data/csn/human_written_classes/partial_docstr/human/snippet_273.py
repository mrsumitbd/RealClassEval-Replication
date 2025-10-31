import urwid

class Clickable:
    """
    Add a `click` signal which is sent when the item is activated or clicked.

    TODO: make it work on widgets which have other signals.
    """
    signals = ['click']

    def keypress(self, size, key):
        if self._command_map[key] == urwid.ACTIVATE:
            self._emit('click')
            return
        return key

    def mouse_event(self, size, event, button, x, y, focus):
        if button == 1:
            self._emit('click')