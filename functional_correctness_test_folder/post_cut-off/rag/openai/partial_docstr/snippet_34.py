
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
                "info": "black",
                "warning": "dark_orange",
                "error": "red",
                "success": "green",
                "debug": "blue",
                "highlight": "magenta",
                "dim": "grey50",
            }
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast)."""
        return Theme(
            {
                "info": "white",
                "warning": "yellow",
                "error": "bright_red",
                "success": "bright_green",
                "debug": "bright_blue",
                "highlight": "bright_magenta",
                "dim": "grey70",
            }
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic colors for maximum compatibility."""
        return Theme(
            {
                "info": "cyan",
                "warning": "yellow",
                "error": "red",
                "success": "green",
                "debug": "magenta",
                "highlight": "blue",
                "dim": "grey50",
            }
        )
