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
                # General text
                "text": "#111111",
                "title": "bold #0f0f0f",
                "subtitle": "#37474f",
                "muted": "dim #424242",
                "emphasis": "bold #111111",
                "code": "#263238",

                # Semantic roles
                "info": "#0d47a1",
                "warning": "#6d4c41",
                "error": "#7f0000",
                "success": "#1b5e20",
                "debug": "#455a64",
                "hint": "#2e7d32",
                "prompt": "bold #0d47a1",
                "input": "#111111",

                # Data-ish
                "path": "#4a148c",
                "url": "underline #0b5394",
                "number": "#0d47a1",
                "boolean": "#1b5e20",
                "timestamp": "#37474f",

                # Rich repr styles
                "repr.number": "#0d47a1",
                "repr.string": "#1b5e20",
                "repr.path": "#4a148c",
                "repr.url": "underline #0b5394",
                "repr.filename": "#4a148c",
                "repr.tag_name": "#6a1b9a",
                "repr.bool_true": "#1b5e20",
                "repr.bool_false": "#7f0000",
                "repr.none": "#424242",

                # Logging
                "log.time": "#607d8b",
                "log.level": "bold #111111",
                "log.level.debug": "#455a64",
                "log.level.info": "#0d47a1",
                "log.level.warning": "#6d4c41",
                "log.level.error": "bold #7f0000",
                "log.level.critical": "bold #7f0000",

                # Progress
                "progress.description": "#263238",
                "progress.percentage": "bold #111111",
                "progress.remaining": "#455a64",
                "progress.elapsed": "#455a64",
                "progress.speed": "#0d47a1",
            },
            inherit=True,
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast)."""
        return Theme(
            {
                # General text
                "text": "#e0e0e0",
                "title": "bold #ffffff",
                "subtitle": "#b0bec5",
                "muted": "dim #9e9e9e",
                "emphasis": "bold #e0e0e0",
                "code": "#eceff1",

                # Semantic roles
                "info": "#bbdefb",
                "warning": "#ffe082",
                "error": "#ffcdd2",
                "success": "#c8e6c9",
                "debug": "#b0bec5",
                "hint": "#c5e1a5",
                "prompt": "bold #bbdefb",
                "input": "#ffffff",

                # Data-ish
                "path": "#d1c4e9",
                "url": "underline #b3e5fc",
                "number": "#bbdefb",
                "boolean": "#c8e6c9",
                "timestamp": "#90a4ae",

                # Rich repr styles
                "repr.number": "#bbdefb",
                "repr.string": "#c8e6c9",
                "repr.path": "#d1c4e9",
                "repr.url": "underline #b3e5fc",
                "repr.filename": "#d1c4e9",
                "repr.tag_name": "#e1bee7",
                "repr.bool_true": "#c8e6c9",
                "repr.bool_false": "#ffcdd2",
                "repr.none": "#e0e0e0",

                # Logging
                "log.time": "#90a4ae",
                "log.level": "bold #e0e0e0",
                "log.level.debug": "#b0bec5",
                "log.level.info": "#bbdefb",
                "log.level.warning": "#ffe082",
                "log.level.error": "bold #ffcdd2",
                "log.level.critical": "bold #ff8a80",

                # Progress
                "progress.description": "#e0e0e0",
                "progress.percentage": "bold #ffffff",
                "progress.remaining": "#b0bec5",
                "progress.elapsed": "#b0bec5",
                "progress.speed": "#bbdefb",
            },
            inherit=True,
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic colors for maximum compatibility."""
        return Theme(
            {
                # General text
                "text": "default",
                "title": "bold",
                "subtitle": "dim",
                "muted": "dim",
                "emphasis": "bold",
                "code": "white",

                # Semantic roles
                "info": "cyan",
                "warning": "yellow",
                "error": "red",
                "success": "green",
                "debug": "blue",
                "hint": "magenta",
                "prompt": "bold cyan",
                "input": "white",

                # Data-ish
                "path": "magenta",
                "url": "underline cyan",
                "number": "blue",
                "boolean": "green",
                "timestamp": "dim",

                # Rich repr styles
                "repr.number": "blue",
                "repr.string": "green",
                "repr.path": "magenta",
                "repr.url": "underline cyan",
                "repr.filename": "magenta",
                "repr.tag_name": "magenta",
                "repr.bool_true": "green",
                "repr.bool_false": "red",
                "repr.none": "dim",

                # Logging
                "log.time": "dim",
                "log.level": "bold",
                "log.level.debug": "blue",
                "log.level.info": "cyan",
                "log.level.warning": "yellow",
                "log.level.error": "bold red",
                "log.level.critical": "bold red",

                # Progress
                "progress.description": "white",
                "progress.percentage": "bold",
                "progress.remaining": "dim",
                "progress.elapsed": "dim",
                "progress.speed": "cyan",
            },
            inherit=True,
        )
