
from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    background: str
    foreground: str
    accent: str
    error: str
    warning: str
    info: str
    success: str


class AdaptiveColorScheme:

    @staticmethod
    def get_light_background_theme() -> Theme:
        # Light background, dark text, accessible accent colors
        return Theme(
            background="#FFFFFF",   # white
            foreground="#222222",   # almost black
            accent="#0057B7",       # blue
            error="#B00020",        # red
            warning="#E65100",      # orange
            info="#1565C0",         # blue
            success="#2E7D32"       # green
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        '''Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast).'''
        return Theme(
            background="#181A1B",   # very dark gray
            foreground="#F5F5F5",   # near white
            accent="#82AAFF",       # light blue
            error="#FF5370",        # light red
            warning="#FFCB6B",      # yellow/orange
            info="#89DDFF",         # cyan
            success="#C3E88D"       # light green
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        '''Classic colors for maximum compatibility.'''
        return Theme(
            background="black",
            foreground="white",
            accent="cyan",
            error="red",
            warning="yellow",
            info="blue",
            success="green"
        )
