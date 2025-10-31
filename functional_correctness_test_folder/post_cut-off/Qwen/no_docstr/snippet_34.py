
class Theme:
    def __init__(self, background_color, text_color, accent_color):
        self.background_color = background_color
        self.text_color = text_color
        self.accent_color = accent_color


class AdaptiveColorScheme:

    @staticmethod
    def get_light_background_theme() -> Theme:
        return Theme("#FFFFFF", "#000000", "#007BFF")

    @staticmethod
    def get_dark_background_theme() -> Theme:
        return Theme("#121212", "#FFFFFF", "#BB86FC")

    @staticmethod
    def get_classic_theme() -> Theme:
        return Theme("#F5F5F5", "#212121", "#6200EE")
