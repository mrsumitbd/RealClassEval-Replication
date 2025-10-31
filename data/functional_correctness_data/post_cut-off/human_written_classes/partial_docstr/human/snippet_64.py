import json
from datetime import datetime

class LogFormatter:
    """日志格式化器"""

    def __init__(self, config, custom_module_colors=None, custom_level_colors=None):
        self.config = config
        self.level_colors = {'debug': '#FFA500', 'info': '#0000FF', 'success': '#008000', 'warning': '#FFFF00', 'error': '#FF0000', 'critical': '#800080'}
        self.module_colors = {'api': '#00FF00', 'emoji': '#00FF00', 'chat': '#0080FF', 'config': '#FFFF00', 'common': '#FF00FF', 'tools': '#00FFFF', 'lpmm': '#00FFFF', 'plugin_system': '#FF0080', 'experimental': '#FFFFFF', 'person_info': '#008000', 'manager': '#800080', 'llm_models': '#008080', 'plugins': '#800000', 'plugin_api': '#808000', 'remote': '#8000FF'}
        if custom_module_colors:
            self.module_colors.update(custom_module_colors)
        if custom_level_colors:
            self.level_colors.update(custom_level_colors)
        color_text = self.config.get('color_text', 'full')
        if color_text == 'none':
            self.enable_colors = False
            self.enable_module_colors = False
            self.enable_level_colors = False
        elif color_text == 'title':
            self.enable_colors = True
            self.enable_module_colors = True
            self.enable_level_colors = False
        elif color_text == 'full':
            self.enable_colors = True
            self.enable_module_colors = True
            self.enable_level_colors = True
        else:
            self.enable_colors = True
            self.enable_module_colors = True
            self.enable_level_colors = False

    def format_log_entry(self, log_entry):
        """格式化日志条目，返回格式化后的文本和样式标签"""
        timestamp = log_entry.get('timestamp', '')
        level = log_entry.get('level', 'info')
        logger_name = log_entry.get('logger_name', '')
        event = log_entry.get('event', '')
        formatted_timestamp = self.format_timestamp(timestamp)
        parts = []
        tags = []
        log_level_style = self.config.get('log_level_style', 'lite')
        if formatted_timestamp:
            if log_level_style == 'lite' and self.enable_level_colors:
                parts.append(formatted_timestamp)
                tags.append(f'level_{level}')
            else:
                parts.append(formatted_timestamp)
                tags.append('timestamp')
        if log_level_style == 'full':
            level_text = f'[{level.upper():>8}]'
            parts.append(level_text)
            if self.enable_level_colors:
                tags.append(f'level_{level}')
            else:
                tags.append('level')
        elif log_level_style == 'compact':
            level_text = f'[{level.upper()[0]:>8}]'
            parts.append(level_text)
            if self.enable_level_colors:
                tags.append(f'level_{level}')
            else:
                tags.append('level')
        if logger_name:
            module_text = f'[{logger_name}]'
            parts.append(module_text)
            if self.enable_module_colors:
                tags.append(f'module_{logger_name}')
            else:
                tags.append('module')
        if isinstance(event, str):
            parts.append(event)
        elif isinstance(event, dict):
            try:
                parts.append(json.dumps(event, ensure_ascii=False, indent=None))
            except (TypeError, ValueError):
                parts.append(str(event))
        else:
            parts.append(str(event))
        tags.append('message')
        extras = []
        for key, value in log_entry.items():
            if key not in ('timestamp', 'level', 'logger_name', 'event'):
                if isinstance(value, (dict, list)):
                    try:
                        value_str = json.dumps(value, ensure_ascii=False, indent=None)
                    except (TypeError, ValueError):
                        value_str = str(value)
                else:
                    value_str = str(value)
                extras.append(f'{key}={value_str}')
        if extras:
            parts.append(' '.join(extras))
            tags.append('extras')
        return (parts, tags)

    def format_timestamp(self, timestamp):
        """格式化时间戳"""
        if not timestamp:
            return ''
        try:
            if 'T' in timestamp:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            else:
                return timestamp
            date_style = self.config.get('date_style', 'm-d H:i:s')
            format_map = {'Y': '%Y', 'm': '%m', 'd': '%d', 'H': '%H', 'i': '%M', 's': '%S'}
            python_format = date_style
            for php_char, python_char in format_map.items():
                python_format = python_format.replace(php_char, python_char)
            return dt.strftime(python_format)
        except Exception:
            return timestamp