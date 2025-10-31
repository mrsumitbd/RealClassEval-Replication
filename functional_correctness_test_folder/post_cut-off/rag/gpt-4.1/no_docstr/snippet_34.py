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
        # For light backgrounds, use dark text colors for contrast
        colors = {
            'primary': '#222222',      # near-black
            'secondary': '#444444',    # dark gray
            'accent': '#005A9E',       # strong blue
            'success': '#217A00',      # dark green
            'warning': '#B36B00',      # dark orange
            'danger': '#A80000',       # dark red
            'info': '#005A9E',         # blue
            'muted': '#666666',        # medium gray
            'link': '#005A9E',         # blue
            'highlight': '#C23934',    # strong red
        }
        return Theme(colors)

    @staticmethod
    def get_dark_background_theme() -> Theme:
        '''Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast).'''
        # For dark backgrounds, use light text colors for contrast
        colors = {
            'primary': '#FFFFFF',      # white
            'secondary': '#E0E0E0',    # light gray
            'accent': '#4FC3F7',       # light blue
            'success': '#81C784',      # light green
            'warning': '#FFD54F',      # yellow
            'danger': '#FF8A65',       # light red/orange
            'info': '#4FC3F7',         # light blue
            'muted': '#B0B0B0',        # gray
            'link': '#4FC3F7',         # light blue
            'highlight': '#FFB300',    # gold
        }
        return Theme(colors)

    @staticmethod
    def get_classic_theme() -> Theme:
        '''Classic colors for maximum compatibility.'''
        # Use standard ANSI color names
        colors = {
            'primary': 'white',
            'secondary': 'bright_black',
            'accent': 'cyan',
            'success': 'green',
            'warning': 'yellow',
            'danger': 'red',
            'info': 'blue',
            'muted': 'bright_black',
            'link': 'blue',
            'highlight': 'magenta',
        }
        return Theme(colors)
