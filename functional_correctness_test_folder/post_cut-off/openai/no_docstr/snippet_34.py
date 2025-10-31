
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Theme:
    background: Tuple[int, int, int]
    foreground: Tuple[int, int, int]
    accent: Tuple[int, int, int]


class AdaptiveColorScheme:
    @staticmethod
    def get_light_background_theme() -> Theme:
        """Theme optimized for light backgrounds."""
        return Theme(
            background=(255, 255, 255),   # white
            foreground=(0, 0, 0),         # black
            accent=(0, 120, 215)          # blue accent
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Theme optimized for dark backgrounds."""
        return Theme(
            background=(30, 30, 30),      # dark gray
            foreground=(255, 255, 255),   # white
            accent=(0, 150, 136)          # teal accent
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic theme with balanced colors."""
        return Theme(
            background=(240, 240, 240),   # light gray
            foreground=(0, 0, 0),         # black
            accent=(255, 165, 0)          # orange accent
        )
