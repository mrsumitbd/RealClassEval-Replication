from typing import Dict


class Theme:
    """Represents a color theme for terminal text."""

    def __init__(self, colors: Dict[str, str]):
        self.colors = colors

    def get(self, role: str) -> str:
        return self.colors.get(role, self.colors.get('text', ''))


class AdaptiveColorScheme:
    '''Scientifically-based adaptive color schemes with proper contrast ratios.
    IMPORTANT: This only changes FONT/FOREGROUND colors, never background colors.
    The terminal's background remains unchanged - we adapt text colors for readability.
    All color choices follow WCAG AA accessibility standards for contrast ratios.
    '''
    @staticmethod
    def get_light_background_theme() -> Theme:
        '''Font colors optimized for light terminal backgrounds (WCAG AA+ contrast).'''
        # On light backgrounds, use dark text for contrast
        return Theme({
            'text': '#222222',         # near-black
            'muted': '#444444',        # dark gray
            'info': '#005a9e',         # strong blue
            'success': '#007a3d',      # strong green
            'warning': '#b36b00',      # dark orange
            'error': '#a80000',        # dark red
            'accent': '#6b21a8',       # purple
            'link': '#0b3d91',         # blue
        })

    @staticmethod
    def get_dark_background_theme() -> Theme:
        '''Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast).'''
        # On dark backgrounds, use light text for contrast
        return Theme({
            'text': '#f5f5f5',         # near-white
            'muted': '#cccccc',        # light gray
            'info': '#4fc3f7',         # light blue
            'success': '#81c784',      # light green
            'warning': '#ffd54f',      # yellow
            'error': '#ff5252',        # bright red
            'accent': '#ce93d8',       # light purple
            'link': '#90caf9',         # light blue
        })

    @staticmethod
    def get_classic_theme() -> Theme:
        '''Classic colors for maximum compatibility.'''
        return Theme({
            'text': 'white',
            'muted': 'grey',
            'info': 'blue',
            'success': 'green',
            'warning': 'yellow',
            'error': 'red',
            'accent': 'magenta',
            'link': 'cyan',
        })
