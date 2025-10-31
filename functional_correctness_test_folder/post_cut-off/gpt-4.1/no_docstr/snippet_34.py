
from dataclasses import dataclass


@dataclass
class Theme:
    background: str
    foreground: str
    accent: str
    error: str
    success: str


class AdaptiveColorScheme:

    @staticmethod
    def get_light_background_theme() -> Theme:
        return Theme(
            background="#FFFFFF",
            foreground="#222222",
            accent="#1976D2",
            error="#D32F2F",
            success="#388E3C"
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        return Theme(
            background="#181A1B",
            foreground="#E0E0E0",
            accent="#90CAF9",
            error="#EF9A9A",
            success="#A5D6A7"
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        return Theme(
            background="#F0F0F0",
            foreground="#000000",
            accent="#0000FF",
            error="#FF0000",
            success="#008000"
        )
