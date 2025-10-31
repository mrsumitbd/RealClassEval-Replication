
from dataclasses import dataclass


@dataclass
class Theme:
    """Class to hold theme colors."""
    background: str
    text: str
    primary: str
    secondary: str


class AdaptiveColorScheme:
    """Class to generate different color schemes."""

    @staticmethod
    def get_light_background_theme() -> Theme:
        """Returns a theme with a light background."""
        return Theme(
            background="#F7F7F7",
            text="#333333",
            primary="#007bff",
            secondary="#6c757d"
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Returns a theme with a dark background."""
        return Theme(
            background="#333333",
            text="#F7F7F7",
            primary="#66d9ef",
            secondary="#f0e68c"
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        """Returns a classic theme."""
        return Theme(
            background="#FFFFFF",
            text="#000000",
            primary="#008000",
            secondary="#800000"
        )

# Example usage:


def main():
    light_theme = AdaptiveColorScheme.get_light_background_theme()
    dark_theme = AdaptiveColorScheme.get_dark_background_theme()
    classic_theme = AdaptiveColorScheme.get_classic_theme()

    print("Light Theme:", light_theme)
    print("Dark Theme:", dark_theme)
    print("Classic Theme:", classic_theme)


if __name__ == "__main__":
    main()
