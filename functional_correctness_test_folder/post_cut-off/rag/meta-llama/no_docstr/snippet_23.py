
import re
from typing import List, Optional
from urllib.parse import urlparse


class GitHubURLExtractor:
    """提取GitHub URL的工具类"""

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        """从文本中提取GitHub URLs"""
        pattern = r'(https?://(?:www\.)?github\.com/[^\s]+)'
        return re.findall(pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        """从文本中提取目标路径"""
        pattern = r'#L(\d+)(?:-L(\d+))?'
        match = re.search(pattern, text)
        if match:
            start_line = match.group(1)
            end_line = match.group(2) or start_line
            return f'L{start_line}-L{end_line}'
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        """从URL推断仓库名称"""
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) >= 2:
            return f'{path_parts[0]}/{path_parts[1]}'
        return ''
