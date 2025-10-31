
class AdaptiveColorScheme:

    @staticmethod
    def get_light_background_theme() -> 'Theme':
        return Theme(
            background_color="#FFFFFF",
            text_color="#000000",
            primary_color="#4285F4",
            secondary_color="#34A853",
            accent_color="#EA4335"
        )

    @staticmethod
    def get_dark_background_theme() -> 'Theme':
        return Theme(
            background_color="#121212",
            text_color="#FFFFFF",
            primary_color="#8AB4F8",
            secondary_color="#81C995",
            accent_color="#F28B82"
        )

    @staticmethod
    def get_classic_theme() -> 'Theme':
        return Theme(
            background_color="#F5F5F5",
            text_color="#333333",
            primary_color="#1E88E5",
            secondary_color="#43A047",
            accent_color="#E53935"
        )


class Theme:
    def __init__(self, background_color: str, text_color: str, primary_color: str, secondary_color: str, accent_color: str):
        self.background_color = background_color
        self.text_color = text_color
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.accent_color = accent_color
