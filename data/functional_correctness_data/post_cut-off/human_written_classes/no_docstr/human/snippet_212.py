from rich.console import Console
import shutil
from rich.markdown import Markdown

class MarkdownConsoleStream:

    def __init__(self, console: Console=None):
        c, r = shutil.get_terminal_size(fallback=(80, 24))
        c -= 2
        self.console = console or Console(emoji_variant='text', width=c)
        self.height = r - 2
        self._last_lines = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def update(self, markdown_text) -> None:
        new_lines = self._render_to_lines(markdown_text)
        old_lines = self._last_lines
        prefix_length = self._common_prefix_length(old_lines, new_lines)
        prefix_length = max(prefix_length, len(old_lines) - self.height, len(new_lines) - self.height)
        old_suffix_len = len(old_lines) - prefix_length
        new_suffix_len = len(new_lines) - prefix_length
        if old_suffix_len > 0:
            print(f'{ESC}[{old_suffix_len}A', end='')
        changed_count = max(old_suffix_len, new_suffix_len)
        for i in range(changed_count):
            if i < new_suffix_len:
                print(f'{ESC}[2K', end='')
                print(new_lines[prefix_length + i].rstrip())
            else:
                print(f'{ESC}[2K', end='')
        self._last_lines = new_lines

    def _render_to_lines(self, markdown_text: str):
        with self.console.capture() as cap:
            self.console.print(Markdown(markdown_text))
        rendered = cap.get()
        split = []
        for s in [r.rstrip() for r in rendered.rstrip('\n').split('\n')]:
            if s or len(split) == 0 or split[-1]:
                split.append(s)
        return split

    @staticmethod
    def _common_prefix_length(a, b) -> int:
        i = 0
        for x, y in zip(a, b):
            if x != y:
                break
            i += 1
        return i