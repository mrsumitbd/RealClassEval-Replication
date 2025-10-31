import json

class ModuleColoredConsoleRenderer:
    """自定义控制台渲染器，为不同模块提供不同颜色"""

    def __init__(self, colors=True):
        self._colors = colors
        self._config = LOG_CONFIG
        self._level_colors = {'debug': '\x1b[38;5;208m', 'info': '\x1b[38;5;117m', 'success': '\x1b[32m', 'warning': '\x1b[33m', 'error': '\x1b[31m', 'critical': '\x1b[35m'}
        color_text = self._config.get('color_text', 'title')
        if color_text == 'none':
            self._colors = False
        elif color_text == 'title':
            self._enable_module_colors = True
            self._enable_level_colors = False
            self._enable_full_content_colors = False
        elif color_text == 'full':
            self._enable_module_colors = True
            self._enable_level_colors = True
            self._enable_full_content_colors = True
        else:
            self._enable_module_colors = True
            self._enable_level_colors = False
            self._enable_full_content_colors = False

    def __call__(self, logger, method_name, event_dict):
        """渲染日志消息"""
        timestamp = event_dict.get('timestamp', '')
        level = event_dict.get('level', 'info')
        logger_name = event_dict.get('logger_name', '')
        event = event_dict.get('event', '')
        parts = []
        log_level_style = self._config.get('log_level_style', 'lite')
        level_color = self._level_colors.get(level.lower(), '') if self._colors else ''
        if timestamp:
            if log_level_style == 'lite' and level_color:
                timestamp_part = f'{level_color}{timestamp}{RESET_COLOR}'
            else:
                timestamp_part = timestamp
            parts.append(timestamp_part)
        if log_level_style == 'full':
            level_text = level.upper()
            if level_color:
                level_part = f'{level_color}[{level_text:>8}]{RESET_COLOR}'
            else:
                level_part = f'[{level_text:>8}]'
            parts.append(level_part)
        elif log_level_style == 'compact':
            level_text = level.upper()[0]
            if level_color:
                level_part = f'{level_color}[{level_text:>8}]{RESET_COLOR}'
            else:
                level_part = f'[{level_text:>8}]'
            parts.append(level_part)
        module_color = ''
        if self._colors and self._enable_module_colors and logger_name:
            module_color = MODULE_COLORS.get(logger_name, '')
        if logger_name:
            display_name = MODULE_ALIASES.get(logger_name, logger_name)
            if self._colors and self._enable_module_colors:
                if module_color:
                    module_part = f'{module_color}[{display_name}]{RESET_COLOR}'
                else:
                    module_part = f'[{display_name}]'
            else:
                module_part = f'[{display_name}]'
            parts.append(module_part)
        event_content = ''
        if isinstance(event, str):
            event_content = event
        elif isinstance(event, dict):
            try:
                event_content = json.dumps(event, ensure_ascii=False, indent=None)
            except (TypeError, ValueError):
                event_content = str(event)
        else:
            event_content = str(event)
        if self._colors and self._enable_full_content_colors and module_color:
            event_content = f'{module_color}{event_content}{RESET_COLOR}'
        parts.append(event_content)
        extras = []
        for key, value in event_dict.items():
            if key not in ('timestamp', 'level', 'logger_name', 'event', 'module', 'lineno', 'pathname'):
                if isinstance(value, (dict, list)):
                    try:
                        value_str = json.dumps(value, ensure_ascii=False, indent=None)
                    except (TypeError, ValueError):
                        value_str = str(value)
                else:
                    value_str = str(value)
                extra_field = f'{key}={value_str}'
                if self._colors and self._enable_full_content_colors and module_color:
                    extra_field = f'{module_color}{extra_field}{RESET_COLOR}'
                extras.append(extra_field)
        if extras:
            parts.append(' '.join(extras))
        return ' '.join(parts)