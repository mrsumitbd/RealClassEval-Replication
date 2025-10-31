
class Theme:
    def __init__(self, primary_color: str, secondary_color: str, accent_color: str):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.accent_color = accent_color

    def __repr__(self):
        return f"Theme(primary_color={self.primary_color}, secondary_color={self.secondary_color}, accent_color={self.accent_color})"


class AdaptiveColorScheme:
    '''Scientifically-based adaptive color schemes with proper contrast ratios.
    IMPORTANT: This only changes FONT/FOREGROUND colors, never background colors.
    The terminal's background remains unchanged - we adapt text colors for readability.
    All color choices follow WCAG AA accessibility standards for contrast ratios.
    '''
    @staticmethod
    def get_light_background_theme() -> Theme:
        '''Font colors optimized for light terminal backgrounds (WCAG AA+ contrast).'''
        return Theme(primary_color="#000000", secondary_color="#555555", accent_color="#007acc")

    @staticmethod
    def get_dark_background_theme() -> Theme:
        '''Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast).'''
        return Theme(primary_color="#ffffff", secondary_color="#b2b2b2", accent_color="#569cd6")

    @staticmethod
    def get_classic_theme() -> Theme:
        '''Classic colors for maximum compatibility.'''
        return Theme(primary_color="#000000", secondary_color="#808080", accent_color="#0000ff")
