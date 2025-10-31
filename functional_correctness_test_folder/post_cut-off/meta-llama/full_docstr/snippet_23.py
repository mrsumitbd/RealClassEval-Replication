
import re
from typing import List, Optional


class GitHubURLExtractor:
    '''提取GitHub URL的工具类'''
    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        '''从文本中提取GitHub URLs'''
        pattern = r'https?://(?:www\.)?github\.com/[^\s]+'
        return re.findall(pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        '''从文本中提取目标路径'''
        pattern = r'https?://(?:www\.)?github\.com/([^\s]+)'
        match = re.search(pattern, text)
        if match:
            url_path = match.group(1)
            parts = url_path.split('/')
            if len(parts) >= 2:
                return '/'.join(parts[1:])
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        '''从URL推断仓库名称'''
        pattern = r'https?://(?:www\.)?github\.com/([^/]+)/([^/]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(2)
        return ''
