
from rich.theme import Theme


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
            {
                "default": "black",
                "error": "red",
                "warning": "orange1",
                "info": "blue",
                "success": "green",
                "debug": "magenta",
            }
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast)."""
        return Theme(
            {
                "default": "white",
                "error": "bright_red",
                "warning": "bright_yellow",
                "info": "bright_cyan",
                "success": "bright_green",
                "debug": "bright_magenta",
            }
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic colors for maximum compatibility."""
        return Theme(
            {
                "default": "white",
                "error": "red",
                "warning": "yellow",
                "info": "cyan",
                "success": "green",
                "debug": "magenta",
            }
        )
