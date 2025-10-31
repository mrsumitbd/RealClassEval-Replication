import typing

class LineFormatter:
    """
    Class that formats a single line with a list of ordered annotations like so:

            one (two three) four
    FOO ‐‐‐‐└─┘ ││ │ │   ││ │  │
    BAR ‐‐‐‐‐‐‐‐└─────────┘ │  │
    BAZ ‐‐‐‐‐‐‐‐‐└─┘ │   │  │  │
    FOO ‐‐‐‐‐‐‐‐‐‐‐‐‐└───┘  │  │
    BAR ‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐‐└──┘

    """

    def __init__(self, line: str):
        self.line: str = line
        self.max_annotation_size: int = 0
        self.annotations: typing.List[LineAnnotation] = []

    def add_annotation(self, text: str, span: typing.Optional[typing.Tuple[int, int]], annotation_ansi: typing.Union[typing.Sequence[int], int, None]=None, text_foreground: typing.Optional[int]=None, text_background: typing.Optional[int]=None):
        """
        Add an annotation to the line formatter.
        The order in which the annotations are added matters.
        """
        if span and span[0] > span[1]:
            span = (span[1], span[0])
        self.max_annotation_size = max(self.max_annotation_size, len(text))
        self.annotations.append(LineAnnotation(text, span, annotation_ansi, text_foreground, text_background))

    def output(self, use_complex: bool=True, use_ansi: bool=False) -> str:
        """
        Output the line and associated annotations, optionally with color
        """
        lines: typing.List[str] = []
        block = BLOCK_CHARACTERS_FANCY if use_complex else BLOCK_CHARACTERS_SIMPLE
        if use_ansi:
            spans = [(annotation.span, annotation.text_foreground, annotation.text_background) for annotation in self.annotations if annotation.span and (annotation.text_foreground or annotation.text_background)]
            if spans:
                spans.sort(key=lambda s: (s[0][1] - s[0][0], s[0][0]))
                line = [' ' * (self.max_annotation_size + 2)]
                color = (None, None)
                for index, character in enumerate(self.line):
                    foreground = None
                    background = None
                    for span in spans:
                        if span[0][0] <= index <= span[0][1]:
                            if foreground is None and span[1] is not None:
                                foreground = span[1]
                            if background is None and span[2] is not None:
                                background = span[2]
                        if foreground is not None and background is not None:
                            break
                    if (foreground, background) != color:
                        line.append('\x1b[0' + (f';{foreground}' if foreground else '') + (f';{background}' if background else '') + 'm' + character)
                    else:
                        line.append(character)
                    color = (foreground, background)
                if color != (None, None):
                    line.append('\x1b[0m')
                lines.append(''.join(line))
            else:
                lines.append(' ' * (self.max_annotation_size + 2) + self.line)
        else:
            lines.append(' ' * (self.max_annotation_size + 2) + self.line)
        annotation_strokes: typing.List[typing.Tuple[int, int, typing.Union[typing.Sequence[int], int, None]]] = []
        for index, annotation in enumerate(self.annotations):
            if not annotation.text or not annotation.span:
                continue
            annotation_strokes.append((index, annotation.span[0], annotation.annotation_ansi))
            annotation_strokes.append((index, annotation.span[1], annotation.annotation_ansi))
        annotation_strokes.sort(key=lambda s: (s[1], s[0]))

        def to_ansi_text(ansi: typing.Union[typing.Sequence[int], int, None]) -> str:
            if ansi is None:
                return '\x1b[0m'
            if isinstance(ansi, int):
                return f'\x1b[0;{ansi}m'
            return f"\x1b[0;{';'.join((str(x) for x in ansi))}m"
        for index, annotation in enumerate(self.annotations):
            if not annotation.text:
                continue
            if use_ansi:
                line = [f"{to_ansi_text(annotation.annotation_ansi)}{annotation.text.rjust(self.max_annotation_size)} {(block[0] if annotation.span else ' ')}"]
            else:
                line = [f"{annotation.text.rjust(self.max_annotation_size)} {(block[0] if annotation.span else ' ')}"]
            character_index = 0
            color = annotation.annotation_ansi
            for stroke in annotation_strokes:
                if stroke[0] < index or stroke[1] < character_index:
                    continue
                if use_ansi and annotation.span and (character_index < annotation.span[1]) and (color != annotation.annotation_ansi):
                    line.append(to_ansi_text(annotation.annotation_ansi))
                    color = annotation.annotation_ansi
                line.append((' ' if not annotation.span else block[0] if character_index < annotation.span[0] else block[2] if character_index < annotation.span[1] else ' ') * (stroke[1] - character_index))
                stroke_type = block[4] if not annotation.span else block[5] if stroke[1] < annotation.span[0] else block[3] if stroke[1] == annotation.span[1] else block[1] if stroke[1] == annotation.span[0] else block[2] if stroke[1] < annotation.span[1] else block[4]
                if use_ansi:
                    target_color = annotation.annotation_ansi if annotation.span and annotation.span[0] < stroke[1] < annotation.span[1] else stroke[2]
                    if target_color != color:
                        line.append(f'{to_ansi_text(target_color)}{stroke_type}')
                        color = target_color
                    else:
                        line.append(stroke_type)
                else:
                    line.append(stroke_type)
                character_index = stroke[1] + 1
            lines.append(''.join(line))
        return '\n'.join(lines) + ('\x1b[0m' if use_ansi else '')