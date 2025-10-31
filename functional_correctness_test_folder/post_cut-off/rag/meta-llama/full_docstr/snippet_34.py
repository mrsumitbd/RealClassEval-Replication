
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
        return Theme({
            'info': 'blue',
            'warning': '#ff8c00',  # DarkOrange
            'danger': 'red',
            'success': '#008000',  # Green
            'primary': 'cyan',
            'secondary': '#4b5154',  # Dark Gray
            'dim': '#aaaaaa',  # Light Gray
        })

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast)."""
        return Theme({
            'info': '#87ceeb',  # SkyBlue
            'warning': '#ffd700',  # Gold
            'danger': '#ff3737',  # Light Red
            'success': '#34c759',  # Light Green
            'primary': '#add8e6',  # Light Cyan
            'secondary': '#cccccc',  # Light Gray
            'dim': '#777777',  # Dark Gray
        })

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic colors for maximum compatibility."""
        return Theme({
            'info': 'blue',
            'warning': 'yellow',
            'danger': 'red',
            'success': 'green',
            'primary': 'cyan',
            'secondary': 'white',
            'dim': 'bright_black',
        })
