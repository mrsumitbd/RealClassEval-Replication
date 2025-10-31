
from typing import List
from pygame.sprite import Group


class ScreenBufferManager:

    def __init__(self) -> None:
        """
        Initialize the ScreenBufferManager.
        """
        self.renderables = []

    def create_screen_renderable(self, screen_buffer: List[str]) -> Group:
        """
        Create a renderable group from a screen buffer.

        Args:
        screen_buffer (List[str]): A list of strings representing the screen buffer.

        Returns:
        Group: A Pygame Group containing the renderables.
        """
        renderable_group = Group()

        for y, line in enumerate(screen_buffer):
            for x, char in enumerate(line):
                # Assuming you have a Renderable class that takes x, y, and char
                # For demonstration purposes, we'll create a simple Sprite class
                # You should replace this with your actual Renderable class
                renderable = self._create_renderable(x, y, char)
                renderable_group.add(renderable)

        self.renderables.append(renderable_group)
        return renderable_group

    def _create_renderable(self, x: int, y: int, char: str):
        # For demonstration purposes, we'll create a simple Sprite class
        # You should replace this with your actual Renderable class
        class Renderable(pygame.sprite.Sprite):
            def __init__(self, x: int, y: int, char: str):
                super().__init__()
                # Replace with your font rendering
                self.image = pygame.Surface((10, 20))
                self.image.fill((255, 255, 255))  # White color
                font = pygame.font.SysFont('Arial', 20)
                text_surface = font.render(
                    char, True, (0, 0, 0))  # Black color
                self.image.blit(text_surface, (0, 0))
                self.rect = self.image.get_rect(
                    topleft=(x * 10, y * 20))  # Assuming 10x20 pixel size

        return Renderable(x, y, char)
