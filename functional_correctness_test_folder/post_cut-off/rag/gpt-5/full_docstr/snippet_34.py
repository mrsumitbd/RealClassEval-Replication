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
                # Core text
                "text": "#111827",
                "subtle": "#374151",
                "emphasis": "bold #111827",
                "dim": "#4b5563",

                # Status / feedback
                "info": "#1d4ed8",
                "warning": "#92400e",
                "error": "#991b1b",
                "success": "#065f46",
                "debug": "#4b5563",

                # Structure / UI
                "title": "bold #111827",
                "header": "bold #1f2937",
                "subheader": "bold #374151",
                "prompt": "bold #1d4ed8",
                "timestamp": "#6b7280",
                "note": "italic #374151",

                # Data / content
                "key": "bold #111827",
                "value": "#1f2937",
                "number": "#b45309",
                "code": "#0f766e",
                "path": "#115e59",
                "link": "underline #1d4ed8",
                "accent": "#7c3aed",

                # Rich logging levels
                "logging.level.debug": "#1d4ed8",
                "logging.level.info": "#1d4ed8",
                "logging.level.warning": "#92400e",
                "logging.level.error": "#991b1b",
                "logging.level.critical": "bold #7f1d1d",
            }
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast)."""
        return Theme(
            {
                # Core text
                "text": "#e5e7eb",
                "subtle": "#9ca3af",
                "emphasis": "bold #f3f4f6",
                "dim": "#9ca3af",

                # Status / feedback
                "info": "#93c5fd",
                "warning": "#fbbf24",
                "error": "#f87171",
                "success": "#34d399",
                "debug": "#a3a3a3",

                # Structure / UI
                "title": "bold #f3f4f6",
                "header": "bold #e5e7eb",
                "subheader": "bold #d1d5db",
                "prompt": "bold #93c5fd",
                "timestamp": "#9ca3af",
                "note": "italic #e5e7eb",

                # Data / content
                "key": "bold #e5e7eb",
                "value": "#f3f4f6",
                "number": "#fde68a",
                "code": "#5eead4",
                "path": "#67e8f9",
                "link": "underline #93c5fd",
                "accent": "#c4b5fd",

                # Rich logging levels
                "logging.level.debug": "#93c5fd",
                "logging.level.info": "#93c5fd",
                "logging.level.warning": "#fbbf24",
                "logging.level.error": "#f87171",
                "logging.level.critical": "bold #fecaca",
            }
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic colors for maximum compatibility."""
        return Theme(
            {
                # Core text
                "text": "white",
                "subtle": "bright_black",
                "emphasis": "bold white",
                "dim": "dim white",

                # Status / feedback
                "info": "blue",
                "warning": "yellow",
                "error": "red",
                "success": "green",
                "debug": "cyan",

                # Structure / UI
                "title": "bold white",
                "header": "bold white",
                "subheader": "bold bright_black",
                "prompt": "bold cyan",
                "timestamp": "bright_black",
                "note": "italic white",

                # Data / content
                "key": "bold white",
                "value": "white",
                "number": "yellow",
                "code": "cyan",
                "path": "cyan",
                "link": "underline cyan",
                "accent": "magenta",

                # Rich logging levels
                "logging.level.debug": "cyan",
                "logging.level.info": "blue",
                "logging.level.warning": "yellow",
                "logging.level.error": "red",
                "logging.level.critical": "bold red",
            }
        )
