
class AdaptiveColorScheme:

    @staticmethod
    def get_light_background_theme() -> Theme:
        return Theme(
            background="#FFFFFF",
            text="#000000",
            primary="#1E88E5",
            secondary="#FFC107",
            accent="#4CAF50"
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        return Theme(
            background="#121212",
            text="#E0E0E0",
            primary="#BB86FC",
            secondary="#03DAC6",
            accent="#CF6679"
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        return Theme(
            background="#F5F5F5",
            text="#212121",
            primary="#3F51B5",
            secondary="#FF5722",
            accent="#009688"
        )
