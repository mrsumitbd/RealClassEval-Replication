
import re
from typing import List, Optional


class GitHubURLExtractor:
    '''提取GitHub URL的工具类'''
    GITHUB_URL_PATTERN = re.compile(
        r'https?://github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9_-]+')
    TARGET_PATH_PATTERN = re.compile(r'target=(\/[a-zA-Z0-9._-]+)+')

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        '''从文本中提取GitHub URLs'''
        return GitHubURLExtractor.GITHUB_URL_PATTERN.findall(text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        '''从文本中提取目标路径'''
        match = GitHubURLExtractor.TARGET_PATH_PATTERN.search(text)
        return match.group(1) if match else None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        '''从URL推断仓库名称'''
        parts = url.strip('/').split('/')
        if len(parts) >= 5 and parts[2] == 'github.com':
            return parts[4]
        raise ValueError("Invalid GitHub URL format")
