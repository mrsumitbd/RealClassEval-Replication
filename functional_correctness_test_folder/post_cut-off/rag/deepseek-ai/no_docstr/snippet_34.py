
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
            primary="#005f87",
            secondary="#5f5faf",
            success="#006700",
            warning="#af5f00",
            error="#d70000",
            info="#0087af",
            highlight="#8700af",
            muted="#767676"
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast)."""
        return Theme(
            primary="#5fafff",
            secondary="#af87ff",
            success="#5fff5f",
            warning="#ffaf5f",
            error="#ff5f5f",
            info="#5fd7ff",
            highlight="#ff87ff",
            muted="#a8a8a8"
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic colors for maximum compatibility."""
        return Theme(
            primary="#0000ff",
            secondary="#6a5acd",
            success="#008000",
            warning="#ffa500",
            error="#ff0000",
            info="#1e90ff",
            highlight="#ff00ff",
            muted="#808080"
        )
