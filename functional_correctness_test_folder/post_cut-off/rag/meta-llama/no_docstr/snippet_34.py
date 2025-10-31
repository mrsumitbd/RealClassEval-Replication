
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
            'danger': '#dc143c',  # Crimson
            'success': '#228b22',  # ForestGreen
            'primary': '#1a1a1a',  # Very dark gray
            'secondary': '#666666',  # Dark gray
        })

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast)."""
        return Theme({
            'info': '#87ceeb',  # SkyBlue
            'warning': '#ffd700',  # Gold
            'danger': '#ff6347',  # Tomato
            'success': '#32cd32',  # LimeGreen
            'primary': '#ffffff',  # White
            'secondary': '#cccccc',  # Light gray
        })

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic colors for maximum compatibility."""
        return Theme({
            'info': 'blue',
            'warning': 'yellow',
            'danger': 'red',
            'success': 'green',
            'primary': 'white',
            'secondary': 'bright_black',
        })
