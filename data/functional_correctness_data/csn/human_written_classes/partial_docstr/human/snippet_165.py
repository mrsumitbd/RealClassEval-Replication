class _ContentManager:
    """Basic Content Manager for tikzplotlib

    This manager uses a dictionary to map z-order to an array of content
    to be drawn at the z-order.
    """

    def __init__(self):
        self._content = dict()

    def extend(self, content, zorder):
        """Extends with a list and a z-order"""
        if zorder not in self._content:
            self._content[zorder] = []
        self._content[zorder].extend(content)

    def flatten(self):
        content_out = []
        all_z = sorted(self._content.keys())
        for z in all_z:
            content_out.extend(self._content[z])
        return content_out