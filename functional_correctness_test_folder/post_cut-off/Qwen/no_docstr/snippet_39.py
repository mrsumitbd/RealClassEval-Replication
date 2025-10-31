
from typing import List
from rich.console import Group


class ScreenBufferManager:

    def __init__(self) -> None:
        pass

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        return Group(*screen_buffer)
