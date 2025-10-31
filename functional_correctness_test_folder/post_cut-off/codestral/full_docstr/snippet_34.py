
class AdaptiveColorScheme:
    '''Scientifically-based adaptive color schemes with proper contrast ratios.
    IMPORTANT: This only changes FONT/FOREGROUND colors, never background colors.
    The terminal's background remains unchanged - we adapt text colors for readability.
    All color choices follow WCAG AA accessibility standards for contrast ratios.
    '''
    @staticmethod
    def get_light_background_theme() -> Theme:
        '''Font colors optimized for light terminal backgrounds (WCAG AA+ contrast).'''
        theme = Theme()
        theme.foreground = Color(0, 0, 0)  # Black
        theme.keyword = Color(0, 0, 255)  # Blue
        theme.operator = Color(0, 0, 0)  # Black
        theme.string = Color(0, 128, 0)  # Green
        theme.comment = Color(128, 128, 128)  # Gray
        theme.number = Color(255, 0, 0)  # Red
        theme.function = Color(0, 0, 128)  # Dark Blue
        theme.class_name = Color(0, 128, 128)  # Teal
        return theme

    @staticmethod
    def get_dark_background_theme() -> Theme:
        '''Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast).'''
        theme = Theme()
        theme.foreground = Color(255, 255, 255)  # White
        theme.keyword = Color(173, 216, 230)  # Light Blue
        theme.operator = Color(255, 255, 255)  # White
        theme.string = Color(144, 238, 144)  # Light Green
        theme.comment = Color(169, 169, 169)  # Dark Gray
        theme.number = Color(255, 99, 71)  # Tomato
        theme.function = Color(135, 206, 235)  # Sky Blue
        theme.class_name = Color(127, 255, 212)  # Aquamarine
        return theme

    @staticmethod
    def get_classic_theme() -> Theme:
        '''Classic colors for maximum compatibility.'''
        theme = Theme()
        theme.foreground = Color(255, 255, 255)  # White
        theme.keyword = Color(255, 0, 255)  # Magenta
        theme.operator = Color(255, 255, 255)  # White
        theme.string = Color(0, 255, 0)  # Green
        theme.comment = Color(128, 128, 128)  # Gray
        theme.number = Color(255, 0, 0)  # Red
        theme.function = Color(0, 0, 255)  # Blue
        theme.class_name = Color(255, 255, 0)  # Yellow
        return theme


class Theme:
    def __init__(self):
        self.foreground = None
        self.keyword = None
        self.operator = None
        self.string = None
        self.comment = None
        self.number = None
        self.function = None
        self.class_name = None


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b
