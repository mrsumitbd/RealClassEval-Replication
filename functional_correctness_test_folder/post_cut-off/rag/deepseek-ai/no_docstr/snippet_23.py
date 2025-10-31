
import re
from typing import List, Optional


class GitHubURLExtractor:
    '''提取GitHub URL的工具类'''
    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        '''从文本中提取GitHub URLs'''
        pattern = r'https?://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/?'
        return re.findall(pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        '''从文本中提取目标路径'''
        pattern = r'https?://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/(?:tree|blob)/[a-zA-Z0-9_.-]+/([a-zA-Z0-9_./-]*)'
        match = re.search(pattern, text)
        return match.group(1) if match else None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        '''从URL推断仓库名称'''
        pattern = r'https?://github\.com/([a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+)'
        match = re.search(pattern, url)
        return match.group(1) if match else ''
