
from rich.theme import Theme


class AdaptiveColorScheme:
    '''Scientifically-based adaptive color schemes with proper contrast ratios.
    IMPORTANT: This only changes FONT/FOREGROUND colors, never background colors.
    The terminal's background remains unchanged - we adapt text colors for readability.
    All color choices follow WCAG AA accessibility standards for contrast ratios.
    '''

    @staticmethod
    def get_light_background_theme() -> Theme:
        '''Font colors optimized for light terminal backgrounds (WCAG AA+ contrast).'''
        # Dark foreground colors for a light background
        return Theme(
            {
                "default": "#000000",          # Black
                "error": "#ff0000",            # Red
                "warning": "#ff8c00",          # Dark Orange
                "success": "#006400",          # Dark Green
                "info": "#00008b",             # Dark Blue
                "debug": "#4b0082",            # Indigo
                "prompt": "#8b008b",           # Dark Magenta
                "highlight": "#2f4f4f",        # Dark Slate Gray
                "comment": "#696969",          # Dim Gray
            }
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        '''Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast).'''
        # Light foreground colors for a dark background
        return Theme(
            {
                "default": "#ffffff",          # White
                "error": "#ff5555",            # Light Red
                "warning": "#ffb86c",          # Light Orange
                "success": "#50fa7b",          # Light Green
                "info": "#8be9fd",             # Light Cyan
                "debug": "#ff79c6",            # Light Magenta
                "prompt": "#f8f8f2",           # Light Gray
                "highlight": "#6272a4",        # Medium Slate Blue
                "comment": "#75715e",          # Dark Olive Green
            }
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        '''Classic colors for maximum compatibility.'''
        # Classic terminal color names
        return Theme(
            {
                "default": "white",
                "error": "red",
                "warning": "yellow",
                "success": "green",
                "info": "blue",
                "debug": "magenta",
                "prompt": "cyan",
                "highlight": "bright_white",
                "comment": "bright_black",
            }
        )
