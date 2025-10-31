
from rich.theme import Theme


class AdaptiveColorScheme:
    """
    Provides pre‑defined Rich Theme objects for different terminal background
    conditions.  The themes are intentionally simple and focus on readability
    and WCAG AA+ contrast compliance.
    """

    @staticmethod
    def get_light_background_theme() -> Theme:
        """
        Theme optimized for light terminal backgrounds.
        Uses dark foreground colors to maintain contrast.
        """
        return Theme(
            {
                "info": "blue",
                "warning": "dark_orange",
                "error": "red",
                "success": "green",
                "debug": "magenta",
                "critical": "bold red",
                "prompt": "cyan",
                "highlight": "bright_white",
            }
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """
        Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast).
        Uses bright foreground colors to stand out against a dark background.
        """
        return Theme(
            {
                "info": "bright_blue",
                "warning": "bright_yellow",
                "error": "bright_red",
                "success": "bright_green",
                "debug": "bright_magenta",
                "critical": "bold bright_red",
                "prompt": "bright_cyan",
                "highlight": "bright_white",
            }
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        """
        Classic colors for maximum compatibility.
        Uses a balanced palette that works reasonably well on both light
        and dark backgrounds.
        """
        return Theme(
            {
                "info": "cyan",
                "warning": "yellow",
                "error": "red",
                "success": "green",
                "debug": "magenta",
                "critical": "red",
                "prompt": "cyan",
                "highlight": "white",
            }
        )
