from rich.theme import Theme


class AdaptiveColorScheme:
    '''Scientifically-based adaptive color schemes with proper contrast ratios.
    IMPORTANT: This only changes FONT/FOREGROUND colors, never background colors.
    The terminal's background remains unchanged - we adapt text colors for readability.
    All color choices follow WCAG AA accessibility standards for contrast ratios.
    '''
    @staticmethod
    def get_light_background_theme() -> Theme:
        '''Font colors optimized for light terminal backgrounds (WCAG AA+ contrast).'''
        return Theme(
            {
                # General purpose
                "primary": "#0B3D91",
                "secondary": "#375A7F",
                "emphasis": "bold",
                "muted": "#555555",
                "dim": "dim",
                "highlight": "bold underline",
                "link": "underline #0A3D91",

                # Status/levels
                "info": "#0B5FA5",
                "success": "#1B6E20",
                "warning": "#8A6D00",
                "error": "#8B0000",
                "critical": "bold #7A0000",
                "debug": "#5A5A5A",
                "notice": "#5C3D99",

                # Headings
                "heading": "bold #232323",
                "subheading": "bold #444444",

                # Code-ish scopes
                "code": "#2A2A2A",
                "code.keyword": "#7A3E9D",
                "code.string": "#005F5F",
                "code.number": "#7A2D00",
                "code.comment": "italic #6A737D",
                "code.name": "#0F3D5E",
            }
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        '''Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast).'''
        return Theme(
            {
                # General purpose
                "primary": "#9CDCFE",
                "secondary": "#CE9178",
                "emphasis": "bold",
                "muted": "#BBBBBB",
                "dim": "dim",
                "highlight": "bold underline",
                "link": "underline #64B5F6",

                # Status/levels
                "info": "#4FC3F7",
                "success": "#A5D6A7",
                "warning": "#FFD54F",
                "error": "#EF9A9A",
                "critical": "bold #FF6B6B",
                "debug": "#B0BEC5",
                "notice": "#C5A3FF",

                # Headings
                "heading": "bold #EAEAEA",
                "subheading": "bold #CFCFCF",

                # Code-ish scopes
                "code": "#E0E0E0",
                "code.keyword": "#C586C0",
                "code.string": "#C3E88D",
                "code.number": "#F78C6C",
                "code.comment": "italic #7F8C8D",
                "code.name": "#9CDCFE",
            }
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        '''Classic colors for maximum compatibility.'''
        return Theme(
            {
                # General purpose
                "primary": "white",
                "secondary": "bright_white",
                "emphasis": "bold",
                "muted": "bright_black",
                "dim": "dim",
                "highlight": "bold underline",
                "link": "underline blue",

                # Status/levels
                "info": "blue",
                "success": "green",
                "warning": "yellow",
                "error": "red",
                "critical": "bold red",
                "debug": "bright_black",
                "notice": "magenta",

                # Headings
                "heading": "bold white",
                "subheading": "bold bright_white",

                # Code-ish scopes
                "code": "white",
                "code.keyword": "magenta",
                "code.string": "green",
                "code.number": "yellow",
                "code.comment": "italic bright_black",
                "code.name": "cyan",
            }
        )
