from typing import TYPE_CHECKING, Callable, Optional, Tuple, Any
from asciimatics.utilities import BoxTool
from asciimatics.widgets.scrollbar import _ScrollBar
from wcwidth import wcswidth

class _BorderManager:

    def __init__(self, frame: 'Frame', has_border: bool, can_scroll: bool):
        """
        Helper class to manage the border and scroll bar attached to a frame.
        Allows for different character to be used in the border and the
        changes in sizing requirements with borders on and off with scroll
        bars on and off.

        :param frame: frame being manager
        :param has_border: True if the frame has a border
        :param can_scroll: True if the frame has a scroll bar
        """
        self._frame = frame
        self.has_border = has_border
        self.scroll_bar = None
        self.box = BoxTool(frame.canvas.unicode_aware)
        if can_scroll:
            scroll_y = 2
            scroll_height = frame.canvas.height - 4
            if not has_border:
                scroll_height = frame.canvas.height - 2
                scroll_y = 1
            self.scroll_bar = _ScrollBar(frame.canvas, frame.palette, frame.canvas.width - 1, scroll_y, scroll_height, frame.get_scroll_pos, frame.set_scroll_pos, absolute=True)
        self.string_len = wcswidth if frame._canvas.unicode_aware else len

    @property
    def can_scroll(self) -> bool:
        return self.scroll_bar is not None

    def get_rectangle(self) -> Tuple[int, int, int, int]:
        """
        Returns the bounding box defined by the usable space left after
        borders and/or scroll bars are accounted for.

        :returns: Tuple containing, x, y, height and width of bounding box
        """
        if self.has_border:
            x = 1
            y = self._frame.canvas.start_line + 1
            h = self._frame.canvas.height - 2
            w = self._frame.canvas.width - 2
        else:
            x = 0
            y = self._frame.canvas.start_line
            h = self._frame.canvas.height
            w = self._frame.canvas.width
            if self.can_scroll:
                w -= 1
        return (x, y, h, w)

    def draw(self):
        """
        Draws the border and/or scroll bars onto the frame managed by this
        object.
        """
        frame = self._frame
        if self.has_border:
            colour, attr, bg = frame.palette['borders']
            for dy in range(frame.canvas.height):
                y = frame.canvas.start_line + dy
                if dy == 0:
                    frame.canvas.print_at(self.box.box_top(frame.canvas.width), 0, y, colour, attr, bg)
                elif dy == frame.canvas.height - 1:
                    frame.canvas.print_at(self.box.box_bottom(frame.canvas.width), 0, y, colour, attr, bg)
                else:
                    frame.canvas.print_at(self.box.v, 0, y, colour, attr, bg)
                    frame.canvas.print_at(self.box.v, frame.canvas.width - 1, y, colour, attr, bg)
            colour, attr, bg = frame.palette['title']
            title_width = self.string_len(frame.title)
            frame.canvas.print_at(frame.title, (frame.canvas.width - title_width) // 2, frame.canvas.start_line, colour, attr, bg)
        if self.can_scroll and self.scroll_bar and (frame.canvas.height > 5):
            self.scroll_bar.update()