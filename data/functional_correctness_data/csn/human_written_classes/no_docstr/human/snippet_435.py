import rich

class IndentedParagraph:

    def __init__(self, renderable, left=4, right=0, first=None):
        self.renderable = renderable
        self.left = left
        self.right = right
        if first is not None:
            self.first = first
        else:
            self.first = self.left

    def __rich_console__(self, console, options):
        style = console.get_style('none')
        width = options.max_width
        render_options = options.update_width(width - self.left - self.right)
        lines = console.render_lines(self.renderable, render_options, style=style, pad=True)
        _Segment = rich.segment.Segment
        left = _Segment(' ' * self.left, style) if self.left else None
        first = _Segment(' ' * self.first, style) if self.left else None
        right = [_Segment(f"{' ' * self.right}", style), _Segment.line()] if self.right else [_Segment.line()]
        for ix, line in enumerate(lines):
            if ix == 0:
                yield first
            else:
                yield left
            yield from line
            yield from right