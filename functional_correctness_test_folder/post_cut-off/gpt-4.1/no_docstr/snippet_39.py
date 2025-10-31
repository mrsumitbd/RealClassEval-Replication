
from typing import List
from rich.console import Group
from rich.text import Text


class ScreenBufferManager:

    def __init__(self) -> None:
        pass

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        lines = [Text(line) for line in screen_buffer]
        return Group(*lines)
