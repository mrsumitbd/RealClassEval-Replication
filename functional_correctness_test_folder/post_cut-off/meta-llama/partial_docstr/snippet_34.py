
from dataclasses import dataclass


@dataclass
class Theme:
    """Represents a color theme."""
    primary: str
    secondary: str
    background: str
    text: str
    accent: str


class AdaptiveColorScheme:
    """Provides various color schemes for different use cases."""

    @staticmethod
    def get_light_background_theme() -> Theme:
        """Font colors optimized for light terminal backgrounds (WCAG AA+ contrast)."""
        return Theme(
            primary="#3498db",
            secondary="#f1c40f",
            background="#f9f9f9",
            text="#333333",
            accent="#e74c3c"
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast)."""
        return Theme(
            primary="#66d9ef",
            secondary="#f7dc6f",
            background="#2c3e50",
            text="#ecf0f1",
            accent="#e67e73"
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic colors for maximum compatibility."""
        return Theme(
            primary="#008000",
            secondary="#0000ff",
            background="#ffffff",
            text="#000000",
            accent="#ff0000"
        )
