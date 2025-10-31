import re
from typing import List, Optional


class GitHubURLExtractor:
    '''提取GitHub URL的工具类'''

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        '''从文本中提取GitHub URLs'''
        # 匹配 https://github.com/owner/repo 或 https://github.com/owner/repo/...
        pattern = re.compile(
            r'https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:[/?#][^\s]*)?')
        return pattern.findall(text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        '''从文本中提取目标路径'''
        # 假设目标路径格式为 Target path: <path> 或 Target: <path>
        match = re.search(
            r'(?:Target path|Target)\s*[:：]\s*([^\s]+)', text, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        '''从URL推断仓库名称'''
        # 只提取 owner/repo
        match = re.match(
            r'https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)', url)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
        return ""
