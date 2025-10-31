
import re
from typing import List, Optional


class GitHubURLExtractor:
    '''提取GitHub URL的工具类'''
    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        '''从文本中提取GitHub URLs'''
        # Regex to match GitHub URLs (http(s)://github.com/owner/repo[...])
        pattern = r'https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:[/?#][^\s]*)?'
        return re.findall(pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        '''从文本中提取目标路径'''
        # Look for "path: ..." or "路径: ..." or "target path: ..." (case-insensitive)
        pattern = r'(?:path|路径|target path)\s*[:：]\s*([^\s]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        '''从URL推断仓库名称'''
        # Extract owner/repo from the URL
        pattern = r'github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)'
        match = re.search(pattern, url)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
        return ""
