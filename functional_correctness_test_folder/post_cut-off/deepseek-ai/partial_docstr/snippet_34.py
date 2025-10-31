
class AdaptiveColorScheme:

    @staticmethod
    def get_light_background_theme() -> Theme:
        return Theme(
            background="#FFFFFF",
            text="#000000",
            primary="#1E88E5",
            secondary="#FF5722",
            accent="#4CAF50",
            error="#F44336",
            warning="#FFC107"
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        '''Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast).'''
        return Theme(
            background="#121212",
            text="#E0E0E0",
            primary="#90CAF9",
            secondary="#FFAB91",
            accent="#81C784",
            error="#E57373",
            warning="#FFD54F"
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        '''Classic colors for maximum compatibility.'''
        return Theme(
            background="#000000",
            text="#FFFFFF",
            primary="#0000FF",
            secondary="#FF0000",
            accent="#00FF00",
            error="#FF0000",
            warning="#FFFF00"
        )
