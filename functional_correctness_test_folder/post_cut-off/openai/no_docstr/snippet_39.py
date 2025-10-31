
from typing import List
from rich.console import Group
from rich.text import Text


class ScreenBufferManager:
    def __init__(self) -> None:
        # Initialize an empty buffer list (optional, can be used for future extensions)
        self.buffer: List[str] = []

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        """
        Convert a list of string lines into a Rich Group renderable.

        Parameters
        ----------
        screen_buffer : List[str]
            A list where each element represents a line of text to be displayed.

        Returns
        -------
        Group
            A Rich Group containing Text objects for each line.
        """
        # Convert each line into a Text object and pack them into a Group
        return Group(*[Text(line) for line in screen_buffer])
