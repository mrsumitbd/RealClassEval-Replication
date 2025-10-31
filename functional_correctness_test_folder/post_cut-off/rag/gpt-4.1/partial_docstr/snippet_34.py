from typing import Dict


class Theme:
    """Simple Theme class to hold color mappings."""

    def __init__(self, colors: Dict[str, str]):
        self.colors = colors

    def __getitem__(self, item):
        return self.colors[item]

    def get(self, item, default=None):
        return self.colors.get(item, default)

    def items(self):
        return self.colors.items()


class AdaptiveColorScheme:
    '''Scientifically-based adaptive color schemes with proper contrast ratios.
    IMPORTANT: This only changes FONT/FOREGROUND colors, never background colors.
    The terminal's background remains unchanged - we adapt text colors for readability.
    All color choices follow WCAG AA accessibility standards for contrast ratios.
    '''
    @staticmethod
    def get_light_background_theme() -> Theme:
        '''Font colors optimized for light terminal backgrounds (WCAG AA+ contrast).'''
        # For light backgrounds, use dark text for contrast
        colors = {
            'primary': '#222222',      # near-black
            'secondary': '#444444',    # dark gray
            'accent': '#005A9E',       # strong blue
            'success': '#217A3C',      # dark green
            'warning': '#B36B00',      # dark orange
            'error': '#A4262C',        # dark red
            'info': '#235A97',         # blue
            'muted': '#666666',        # medium gray
            'link': '#0B3D91',         # blue, accessible
        }
        return Theme(colors)

    @staticmethod
    def get_dark_background_theme() -> Theme:
        '''Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast).'''
        # For dark backgrounds, use light text for contrast
        colors = {
            'primary': '#F3F3F3',      # near-white
            'secondary': '#CCCCCC',    # light gray
            'accent': '#4FC3F7',       # light blue
            'success': '#7FFFD4',      # aquamarine
            'warning': '#FFD700',      # gold
            'error': '#FF6F61',        # light red
            'info': '#81D4FA',         # light blue
            'muted': '#AAAAAA',        # gray
            'link': '#82B1FF',         # light blue
        }
        return Theme(colors)

    @staticmethod
    def get_classic_theme() -> Theme:
        '''Classic colors for maximum compatibility.'''
        colors = {
            'primary': 'white',
            'secondary': 'bright_white',
            'accent': 'cyan',
            'success': 'green',
            'warning': 'yellow',
            'error': 'red',
            'info': 'blue',
            'muted': 'bright_black',
            'link': 'blue',
        }
        return Theme(colors)
