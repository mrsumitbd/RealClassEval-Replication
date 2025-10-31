from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    name: str
    background: str
    foreground: str
    primary: str
    secondary: str
    accent: str
    info: str
    success: str
    warning: str
    error: str
    border: str
    muted: str
    link: str
    code_bg: str
    code_fg: str
    shadow: str


class AdaptiveColorScheme:

    @staticmethod
    def get_light_background_theme() -> Theme:
        return Theme(
            name="Light",
            background="#FFFFFF",
            foreground="#1F2937",
            primary="#2563EB",
            secondary="#6B7280",
            accent="#10B981",
            info="#0EA5E9",
            success="#16A34A",
            warning="#D97706",
            error="#DC2626",
            border="#E5E7EB",
            muted="#F3F4F6",
            link="#1D4ED8",
            code_bg="#F6F8FA",
            code_fg="#0F172A",
            shadow="rgba(0,0,0,0.08)",
        )

    @staticmethod
    def get_dark_background_theme() -> Theme:
        return Theme(
            name="Dark",
            background="#0B1220",
            foreground="#E5E7EB",
            primary="#60A5FA",
            secondary="#9CA3AF",
            accent="#34D399",
            info="#38BDF8",
            success="#22C55E",
            warning="#F59E0B",
            error="#F87171",
            border="#1F2937",
            muted="#111827",
            link="#93C5FD",
            code_bg="#0F172A",
            code_fg="#E2E8F0",
            shadow="rgba(0,0,0,0.4)",
        )

    @staticmethod
    def get_classic_theme() -> Theme:
        return Theme(
            name="Classic",
            background="#F5F5F5",
            foreground="#000000",
            primary="#0000FF",
            secondary="#808080",
            accent="#008000",
            info="#0000CC",
            success="#007700",
            warning="#CC7A00",
            error="#CC0000",
            border="#C0C0C0",
            muted="#E6E6E6",
            link="#0000EE",
            code_bg="#FFFFE0",
            code_fg="#000080",
            shadow="rgba(0,0,0,0.15)",
        )
