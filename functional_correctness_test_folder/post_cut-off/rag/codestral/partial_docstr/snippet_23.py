
import re
from typing import List, Optional


class GitHubURLExtractor:
    '''提取GitHub URL的工具类'''

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        '''从文本中提取GitHub URLs'''
        pattern = r'https?://(?:www\.)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:/[^/\s]*)?'
        return re.findall(pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        '''从文本中提取目标路径'''
        urls = GitHubURLExtractor.extract_github_urls(text)
        if not urls:
            return None
        url = urls[0]
        path_match = re.search(r'github\.com/[^/]+/[^/]+/(.*)', url)
        return path_match.group(1) if path_match else None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        '''从URL推断仓库名称'''
        match = re.search(r'github\.com/([^/]+/[^/]+)', url)
        if not match:
            raise ValueError("Invalid GitHub URL")
        return match.group(1)
