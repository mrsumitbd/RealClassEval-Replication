from typing import List
from rich.console import Group
from rich.text import Text


class ScreenBufferManager:
    def __init__(self) -> None:
        pass

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        if not screen_buffer:
            return Group()
        texts = []
        last_index = len(screen_buffer) - 1
        for i, line in enumerate(screen_buffer):
            t = Text(line)
            if i != last_index:
                t.append("\n")
            texts.append(t)
        return Group(*texts)
