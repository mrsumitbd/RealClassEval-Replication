
class AdaptiveColorScheme:

    @staticmethod
    def get_light_background_theme() -> Theme:
        return Theme(
            background_color='white',
            foreground_color='black',
            keyword_color='blue',
            string_color='green',
            comment_color='gray',
            number_color='purple'
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        '''Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast).'''
        return Theme(
            background_color='black',
            foreground_color='white',
            keyword_color='light_blue',
            string_color='light_green',
            comment_color='light_gray',
            number_color='light_purple'
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        '''Classic colors for maximum compatibility.'''
        return Theme(
            background_color='white',
            foreground_color='black',
            keyword_color='blue',
            string_color='green',
            comment_color='gray',
            number_color='purple'
        )


class Theme:
    def __init__(self, background_color, foreground_color, keyword_color, string_color, comment_color, number_color):
        self.background_color = background_color
        self.foreground_color = foreground_color
        self.keyword_color = keyword_color
        self.string_color = string_color
        self.comment_color = comment_color
        self.number_color = number_color
