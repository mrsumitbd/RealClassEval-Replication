from rich.theme import Theme


class AdaptiveColorScheme:
    @staticmethod
    def get_light_background_theme() -> Theme:
        return Theme(
            {
                "text": "color(16)",
                "muted": "color(59)",
                "dim": "color(102)",
                "title": "bold color(18)",
                "subtitle": "bold color(24)",
                "info": "color(19)",
                "hint": "italic color(24)",
                "success": "bold color(22)",
                "warning": "bold color(130)",
                "error": "bold color(124)",
                "critical": "bold reverse color(196)",
                "highlight": "reverse color(24)",
                "primary": "bold color(19)",
                "secondary": "color(60)",
                "accent": "bold color(55)",
                "link": "underline color(19)",
                "debug": "italic color(60)",
            }
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast)."""
        return Theme(
            {
                "text": "white",
                "muted": "grey70",
                "dim": "grey50",
                "title": "bold bright_white",
                "subtitle": "bold grey84",
                "info": "bright_cyan",
                "hint": "italic cyan",
                "success": "bold bright_green",
                "warning": "bold yellow",
                "error": "bold bright_red",
                "critical": "bold reverse bright_red",
                "highlight": "reverse bright_cyan",
                "primary": "bold bright_cyan",
                "secondary": "grey70",
                "accent": "bold bright_magenta",
                "link": "underline bright_cyan",
                "debug": "italic grey62",
            }
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic colors for maximum compatibility."""
        return Theme(
            {
                "text": "white",
                "muted": "bright_black",
                "dim": "bright_black",
                "title": "bold white",
                "subtitle": "bold bright_black",
                "info": "cyan",
                "hint": "italic cyan",
                "success": "green",
                "warning": "yellow",
                "error": "red",
                "critical": "bold reverse red",
                "highlight": "reverse blue",
                "primary": "bold blue",
                "secondary": "bright_black",
                "accent": "magenta",
                "link": "underline blue",
                "debug": "italic bright_black",
            }
        )
