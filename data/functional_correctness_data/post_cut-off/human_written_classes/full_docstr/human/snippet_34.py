from rich.theme import Theme

class AdaptiveColorScheme:
    """Scientifically-based adaptive color schemes with proper contrast ratios.

    IMPORTANT: This only changes FONT/FOREGROUND colors, never background colors.
    The terminal's background remains unchanged - we adapt text colors for readability.

    All color choices follow WCAG AA accessibility standards for contrast ratios.
    """

    @staticmethod
    def get_light_background_theme() -> Theme:
        """Font colors optimized for light terminal backgrounds (WCAG AA+ contrast)."""
        return Theme({'header': 'color(17)', 'info': 'color(19)', 'warning': 'color(166)', 'error': 'color(124)', 'success': 'color(22)', 'value': 'color(235)', 'dim': 'color(243)', 'separator': 'color(240)', 'progress_bar': 'black', 'highlight': 'color(124)', 'cost.low': 'black', 'cost.medium': 'black', 'cost.high': 'black', 'table.border': 'color(238)', 'table.header': 'bold color(17)', 'table.row': 'color(235)', 'table.row.alt': 'color(238)', 'progress.bar.fill': 'black', 'progress.bar': 'black', 'progress.bar.empty': 'color(250)', 'progress.percentage': 'bold color(235)', 'chart.bar': 'color(17)', 'chart.line': 'color(19)', 'chart.point': 'color(124)', 'chart.axis': 'color(240)', 'chart.label': 'color(235)', 'status.active': 'color(22)', 'status.inactive': 'color(243)', 'status.warning': 'color(166)', 'status.error': 'color(124)', 'time.elapsed': 'color(235)', 'time.remaining': 'color(166)', 'time.duration': 'color(19)', 'model.opus': 'color(17)', 'model.sonnet': 'color(19)', 'model.haiku': 'color(22)', 'model.unknown': 'color(243)', 'plan.pro': 'color(166)', 'plan.max5': 'color(19)', 'plan.max20': 'color(17)', 'plan.custom': 'color(22)'})

    @staticmethod
    def get_dark_background_theme() -> Theme:
        """Font colors optimized for dark terminal backgrounds (WCAG AA+ contrast)."""
        return Theme({'header': 'color(117)', 'info': 'color(111)', 'warning': 'color(214)', 'error': 'color(203)', 'success': 'color(118)', 'value': 'color(253)', 'dim': 'color(245)', 'separator': 'color(248)', 'progress_bar': 'white', 'highlight': 'color(203)', 'cost.low': 'white', 'cost.medium': 'white', 'cost.high': 'white', 'table.border': 'color(248)', 'table.header': 'bold color(117)', 'table.row': 'color(253)', 'table.row.alt': 'color(251)', 'progress.bar.fill': 'white', 'progress.bar': 'white', 'progress.bar.empty': 'color(238)', 'progress.percentage': 'bold color(253)', 'chart.bar': 'color(111)', 'chart.line': 'color(117)', 'chart.point': 'color(203)', 'chart.axis': 'color(248)', 'chart.label': 'color(253)', 'status.active': 'color(118)', 'status.inactive': 'color(245)', 'status.warning': 'color(214)', 'status.error': 'color(203)', 'time.elapsed': 'color(253)', 'time.remaining': 'color(214)', 'time.duration': 'color(111)', 'model.opus': 'color(117)', 'model.sonnet': 'color(111)', 'model.haiku': 'color(118)', 'model.unknown': 'color(245)', 'plan.pro': 'color(214)', 'plan.max5': 'color(111)', 'plan.max20': 'color(117)', 'plan.custom': 'color(118)'})

    @staticmethod
    def get_classic_theme() -> Theme:
        """Classic colors for maximum compatibility."""
        return Theme({'header': 'cyan', 'info': 'blue', 'warning': 'yellow', 'error': 'red', 'success': 'green', 'value': 'white', 'dim': 'bright_black', 'separator': 'white', 'progress_bar': 'green', 'highlight': 'red', 'cost.low': 'green', 'cost.medium': 'yellow', 'cost.high': 'red', 'table.border': 'white', 'table.header': 'bold cyan', 'table.row': 'white', 'table.row.alt': 'bright_black', 'progress.bar.fill': 'green', 'progress.bar.empty': 'bright_black', 'progress.percentage': 'bold white', 'chart.bar': 'blue', 'chart.line': 'cyan', 'chart.point': 'red', 'chart.axis': 'white', 'chart.label': 'white', 'status.active': 'green', 'status.inactive': 'bright_black', 'status.warning': 'yellow', 'status.error': 'red', 'time.elapsed': 'white', 'time.remaining': 'yellow', 'time.duration': 'blue', 'model.opus': 'cyan', 'model.sonnet': 'blue', 'model.haiku': 'green', 'model.unknown': 'bright_black', 'plan.pro': 'yellow', 'plan.max5': 'cyan', 'plan.max20': 'blue', 'plan.custom': 'green'})