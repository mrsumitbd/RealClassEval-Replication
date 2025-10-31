
from typing import Dict


class Theme(dict):
    """A simple Theme class inheriting from dict for color mapping."""
    pass


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
        return Theme({
            'primary':      '#222222',  # near-black
            'secondary':    '#444444',  # dark gray
            'accent':       '#005A9E',  # strong blue
            'success':      '#217A0B',  # dark green
            'warning':      '#B36B00',  # dark orange
            'error':        '#B00020',  # dark red
            'info':         '#005A9E',  # blue
            'muted':        '#666666',  # medium gray
            'link':         '#0B3D91',  # accessible blue
            'highlight':    '#000000',  # black
        })

    @staticmethod
    def get_dark_background_theme() -> Theme:
        '''Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast).'''
        # For dark backgrounds, use light text colors for contrast
        return Theme({
            'primary':      '#FFFFFF',  # white
            'secondary':    '#E0E0E0',  # light gray
            'accent':       '#4FC3F7',  # light blue
            'success':      '#81C784',  # light green
            'warning':      '#FFD54F',  # yellow
            'error':        '#FF8A65',  # light red/orange
            'info':         '#4FC3F7',  # light blue
            'muted':        '#B0B0B0',  # gray
            'link':         '#82B1FF',  # accessible blue
            'highlight':    '#FFFFFF',  # white
        })

    @staticmethod
    def get_classic_theme() -> Theme:
        '''Classic colors for maximum compatibility.'''
        return Theme({
            'primary':      'white',
            'secondary':    'bright_white',
            'accent':       'cyan',
            'success':      'green',
            'warning':      'yellow',
            'error':        'red',
            'info':         'blue',
            'muted':        'bright_black',
            'link':         'blue',
            'highlight':    'bright_yellow',
        })
