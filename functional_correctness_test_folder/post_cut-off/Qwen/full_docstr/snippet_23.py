
import re
from typing import List, Optional


class GitHubURLExtractor:
    '''提取GitHub URL的工具类'''
    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        '''从文本中提取GitHub URLs'''
        github_url_pattern = r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+'
        return re.findall(github_url_pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        '''从文本中提取目标路径'''
        path_pattern = r'path=([^\s]+)'
        match = re.search(path_pattern, text)
        return match.group(1) if match else None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        '''从URL推断仓库名称'''
        repo_name_pattern = r'https?://(?:www\.)?github\.com/[a-zA-Z0-9_-]+/([a-zA-Z0-9_-]+)'
        match = re.search(repo_name_pattern, url)
        return match.group(1) if match else ''
