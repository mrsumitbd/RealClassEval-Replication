import re
from typing import Any, Dict, List, Optional

class AppMatcher:
    """
    统一的应用程序匹配器.
    """
    SPECIAL_MAPPINGS = {'qq音乐': ['qqmusic', 'qq音乐', 'qq music'], 'qqmusic': ['qqmusic', 'qq音乐', 'qq music'], 'qq music': ['qqmusic', 'qq音乐', 'qq music'], 'tencent meeting': ['tencent meeting', '腾讯会议', 'voovmeeting'], '腾讯会议': ['tencent meeting', '腾讯会议', 'voovmeeting'], 'google chrome': ['chrome', 'googlechrome', 'google chrome'], 'microsoft edge': ['msedge', 'edge', 'microsoft edge'], 'microsoft office': ['microsoft office', 'office', 'word', 'excel', 'powerpoint'], 'microsoft word': ['microsoft word', 'word'], 'microsoft excel': ['microsoft excel', 'excel'], 'microsoft powerpoint': ['microsoft powerpoint', 'powerpoint'], 'visual studio code': ['code', 'vscode', 'visual studio code'], 'wps office': ['wps', 'wps office'], 'qq': ['qq', 'qqnt', 'tencentqq'], 'wechat': ['wechat', 'weixin', '微信'], 'dingtalk': ['dingtalk', '钉钉', 'ding'], '钉钉': ['dingtalk', '钉钉', 'ding'], 'chrome': ['chrome', 'googlechrome', 'google chrome'], 'firefox': ['firefox', 'mozilla'], 'edge': ['msedge', 'edge', 'microsoft edge'], 'safari': ['safari'], 'notepad': ['notepad', 'notepad++'], 'calculator': ['calc', 'calculator', 'calculatorapp'], 'calc': ['calc', 'calculator', 'calculatorapp'], 'feishu': ['feishu', '飞书', 'lark'], 'vscode': ['code', 'vscode', 'visual studio code'], 'pycharm': ['pycharm', 'pycharm64'], 'cursor': ['cursor'], 'typora': ['typora'], 'wps': ['wps', 'wps office'], 'office': ['microsoft office', 'office', 'word', 'excel', 'powerpoint'], 'word': ['microsoft word', 'word'], 'excel': ['microsoft excel', 'excel'], 'powerpoint': ['microsoft powerpoint', 'powerpoint'], 'finder': ['finder'], 'terminal': ['terminal', 'iterm'], 'iterm': ['iterm', 'iterm2']}
    PROCESS_GROUPS = {'chrome': 'chrome', 'googlechrome': 'chrome', 'firefox': 'firefox', 'edge': 'edge', 'msedge': 'edge', 'safari': 'safari', 'qq': 'qq', 'qqnt': 'qq', 'tencentqq': 'qq', 'qqmusic': 'qqmusic', 'QQMUSIC': 'QQMUSIC', 'QQ音乐': 'QQ音乐', 'wechat': 'wechat', 'weixin': 'wechat', 'dingtalk': 'dingtalk', '钉钉': 'dingtalk', 'feishu': 'feishu', '飞书': 'feishu', 'lark': 'feishu', 'vscode': 'vscode', 'code': 'vscode', 'cursor': 'cursor', 'pycharm': 'pycharm', 'pycharm64': 'pycharm', 'typora': 'typora', 'calculatorapp': 'calculator', 'calc': 'calculator', 'calculator': 'calculator', 'tencent meeting': 'tencent_meeting', '腾讯会议': 'tencent_meeting', 'voovmeeting': 'tencent_meeting', 'wps': 'wps', 'word': 'word', 'excel': 'excel', 'powerpoint': 'powerpoint', 'finder': 'finder', 'terminal': 'terminal', 'iterm': 'iterm', 'iterm2': 'iterm'}

    @classmethod
    def normalize_name(cls, name: str) -> str:
        """
        标准化应用程序名称.
        """
        if not name:
            return ''
        name = name.lower().replace('.exe', '')
        name = re.sub('\\s+v?\\d+[\\.\\d]*', '', name)
        name = re.sub('\\s*\\(\\d+\\)', '', name)
        name = re.sub('\\s*\\[.*?\\]', '', name)
        name = ' '.join(name.split())
        return name.strip()

    @classmethod
    def get_process_group(cls, process_name: str) -> str:
        """
        获取进程所属的分组.
        """
        normalized = cls.normalize_name(process_name)
        if normalized in cls.PROCESS_GROUPS:
            return cls.PROCESS_GROUPS[normalized]
        for key, group in cls.PROCESS_GROUPS.items():
            if key in normalized or normalized in key:
                return group
        return normalized

    @classmethod
    def match_application(cls, target_name: str, app_info: Dict[str, Any]) -> int:
        """匹配应用程序，返回匹配度分数.

        Args:
            target_name: 目标应用名称
            app_info: 应用程序信息

        Returns:
            int: 匹配度分数 (0-100)，0表示不匹配
        """
        if not target_name or not app_info:
            return 0
        target_lower = target_name.lower()
        app_name = app_info.get('name', '').lower()
        display_name = app_info.get('display_name', '').lower()
        window_title = app_info.get('window_title', '').lower()
        exe_path = app_info.get('command', '').lower()
        if target_lower == app_name or target_lower == display_name:
            return 100
        best_special_score = 0
        for key in cls.SPECIAL_MAPPINGS:
            if key in target_lower or target_lower == key:
                for alias in cls.SPECIAL_MAPPINGS[key]:
                    if alias.lower() in app_name or alias.lower() in display_name:
                        if target_lower == key:
                            score = 98
                        elif len(key) > len(target_lower) * 0.8:
                            score = 97
                        else:
                            score = 95
                        if score > best_special_score:
                            best_special_score = score
        if best_special_score > 0:
            return best_special_score
        normalized_target = cls.normalize_name(target_name)
        normalized_app = cls.normalize_name(app_info.get('name', ''))
        normalized_display = cls.normalize_name(app_info.get('display_name', ''))
        if normalized_target == normalized_app or normalized_target == normalized_display:
            return 90
        if target_lower in app_name:
            return 80
        if target_lower in display_name:
            return 75
        if app_name and app_name in target_lower:
            if len(app_name) < len(target_lower) * 0.5:
                return 50
            return 70
        if window_title and target_lower in window_title:
            return 60
        if exe_path and target_lower in exe_path:
            return 50
        if cls._fuzzy_match(target_lower, app_name) or cls._fuzzy_match(target_lower, display_name):
            return 30
        return 0

    @classmethod
    def _fuzzy_match(cls, target: str, candidate: str) -> bool:
        """
        模糊匹配.
        """
        if not target or not candidate:
            return False
        target_clean = re.sub('[^a-zA-Z0-9\\u4e00-\\u9fff]', '', target)
        candidate_clean = re.sub('[^a-zA-Z0-9\\u4e00-\\u9fff]', '', candidate)
        return target_clean in candidate_clean or candidate_clean in target_clean