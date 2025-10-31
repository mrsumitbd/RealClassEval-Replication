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
                # Base text
                "text": "#1a1a1a",
                "primary": "bold #000000",
                "secondary": "#333333",
                "muted": "#555555",

                # Status/severity
                "success": "#0b6e3d",
                "warning": "#8a6d1a",
                "error": "#8b1a1a",
                "critical": "bold #7f0000",
                "info": "#0b5394",
                "debug": "#5a5a5a",
                "notice": "#123c69",

                # Accents
                "accent": "#5a2ca0",
                "highlight": "bold #2c7da0",

                # Headings and semantic elements
                "title": "bold #000000",
                "subtitle": "#1f3a60",
                "link": "underline #0b5394",
                "code": "#1d3557",
            }
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast)."""
        return Theme(
            {
                # Base text
                "text": "#e6e6e6",
                "primary": "bold white",
                "secondary": "#d0d0d0",
                "muted": "bright_black",

                # Status/severity
                "success": "bright_green",
                "warning": "bright_yellow",
                "error": "bright_red",
                "critical": "bold bright_red",
                "info": "bright_cyan",
                "debug": "bright_blue",
                "notice": "bright_magenta",

                # Accents
                "accent": "bright_magenta",
                "highlight": "bold bright_cyan",

                # Headings and semantic elements
                "title": "bold white",
                "subtitle": "bright_cyan",
                "link": "underline bright_blue",
                "code": "#dddddd",
            }
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic colors for maximum compatibility."""
        return Theme(
            {
                # Base text
                "text": "default",
                "primary": "default",
                "secondary": "default",
                "muted": "bright_black",

                # Status/severity
                "success": "green",
                "warning": "yellow",
                "error": "red",
                "critical": "bold red",
                "info": "cyan",
                "debug": "blue",
                "notice": "magenta",

                # Accents and semantics
                "accent": "magenta",
                "highlight": "bold",
                "title": "bold",
                "subtitle": "bold",
                "link": "underline blue",
                "code": "magenta",
            }
        )
