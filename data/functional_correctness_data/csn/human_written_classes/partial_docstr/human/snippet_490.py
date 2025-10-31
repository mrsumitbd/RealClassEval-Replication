import typing

class MultilineFormatter:
    """
    A wrapper around LineFormatter that allows annotating a full block of text.
    """

    def __init__(self, text: str):
        self.lines: typing.List[LineFormatter] = [LineFormatter(line) for line in text.splitlines()]

    def add_annotation(self, line: int, text: str, span: typing.Optional[typing.Tuple[int, int]], annotation_ansi: typing.Union[typing.Sequence[int], int, None]=None, text_foreground: typing.Optional[int]=None, text_background: typing.Optional[int]=None):
        """
        Add an annotation to a line of this formatter.
        The order in which the annotations are added matters.
        """
        self.lines[line].add_annotation(text, span, annotation_ansi, text_foreground, text_background)

    def output(self, use_complex: bool=True, use_ansi: bool=False) -> str:
        """
        Outputs all lines with their annotations
        """
        max_line = max((formatter.max_annotation_size for formatter in self.lines))
        lines: typing.List[str] = []
        for formatter in self.lines:
            formatter.max_annotation_size = max_line
            lines.append(formatter.output(use_complex, use_ansi))
        return '\n'.join(lines)