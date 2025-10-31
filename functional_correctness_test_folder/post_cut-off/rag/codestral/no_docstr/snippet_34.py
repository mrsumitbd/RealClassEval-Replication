
from typing import NamedTuple


class Theme(NamedTuple):
    primary: str
    secondary: str
    success: str
    warning: str
    error: str
    info: str
    debug: str


class AdaptiveColorScheme:
    """Scientifically-based adaptive color schemes with proper contrast ratios.
    IMPORTANT: This only changes FONT/FOREGROUND colors, never background colors.
    The terminal's background remains unchanged - we adapt text colors for readability.
    All color choices follow WCAG AA accessibility standards for contrast ratios.
    """

    @staticmethod
    def get_light_background_theme() -> Theme:
        """Font colors optimized for light terminal backgrounds (WCAG AA+ contrast)."""
        return Theme(
            primary='#000000',      # Black
            secondary='#333333',    # Dark Gray
            success='#006400',      # Dark Green
            warning='#8B4513',     # Saddle Brown
            error='#8B0000',        # Dark Red
            info='#00008B',         # Dark Blue
            debug='#4B0082'         # Indigo
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast)."""
        return Theme(
            primary='#FFFFFF',      # White
            secondary='#CCCCCC',    # Light Gray
            success='#00FF00',      # Green
            warning='#FFA500',     # Orange
            error='#FF0000',        # Red
            info='#00BFFF',        # Deep Sky Blue
            debug='#9370DB'         # Medium Purple
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic colors for maximum compatibility."""
        return Theme(
            primary='#FFFFFF',      # White
            secondary='#CCCCCC',    # Light Gray
            success='#00FF00',      # Green
            warning='#FFFF00',     # Yellow
            error='#FF0000',        # Red
            info='#00FFFF',        # Cyan
            debug='#FF00FF'         # Magenta
        )
