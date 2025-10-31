
class Theme:
    def __init__(self, background_color, font_color, accent_color):
        self.background_color = background_color
        self.font_color = font_color
        self.accent_color = accent_color


class AdaptiveColorScheme:

    @staticmethod
    def get_light_background_theme() -> Theme:
        return Theme("#FFFFFF", "#000000", "#007BFF")

    @staticmethod
    def get_dark_background_theme() -> Theme:
        return Theme("#121212", "#E0E0E0", "#BB86FC")

    @staticmethod
    def get_classic_theme() -> Theme:
        return Theme("#F0F0F0", "#000000", "#0000FF")
