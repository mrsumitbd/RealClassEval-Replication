from typing import List, Dict, Optional, Any
import os
import re

class LocalPathExtractor:
    """本地路径提取器"""

    @staticmethod
    def is_local_path(path: str) -> bool:
        """判断是否为本地路径"""
        path = path.strip('"\'')
        if re.match('^https?://', path, re.IGNORECASE) or re.match('^ftp://', path, re.IGNORECASE):
            return False
        path_indicators = [os.path.sep, '/', '\\', '~', '.', '..']
        has_extension = bool(os.path.splitext(path)[1])
        if any((indicator in path for indicator in path_indicators)) or has_extension:
            expanded_path = os.path.expanduser(path)
            return os.path.exists(expanded_path) or any((indicator in path for indicator in path_indicators))
        return False

    @staticmethod
    def extract_local_paths(text: str) -> List[str]:
        """从文本中提取本地文件路径"""
        patterns = ['"([^"]+)"', "'([^']+)'", '(?:^|\\s)((?:[~./\\\\]|[A-Za-z]:)?(?:[^/\\\\\\s]+[/\\\\])*[^/\\\\\\s]+\\.[A-Za-z0-9]+)(?:\\s|$)', '(?:^|\\s)((?:~|\\.{1,2})?/[^\\s]+)(?:\\s|$)', '(?:^|\\s)([A-Za-z]:[/\\\\][^\\s]+)(?:\\s|$)', '(?:^|\\s)(\\.{1,2}[/\\\\][^\\s]+)(?:\\s|$)']
        local_paths = []
        potential_paths = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            potential_paths.extend(matches)
        for path in potential_paths:
            path = path.strip()
            if path and LocalPathExtractor.is_local_path(path):
                expanded_path = os.path.expanduser(path)
                if expanded_path not in local_paths:
                    local_paths.append(expanded_path)
        return local_paths