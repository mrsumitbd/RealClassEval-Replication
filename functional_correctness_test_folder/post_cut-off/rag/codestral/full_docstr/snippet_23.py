
import re
from typing import List, Optional


class GitHubURLExtractor:
    '''提取GitHub URL的工具类'''

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        '''从文本中提取GitHub URLs'''
        pattern = r'(https?://)?(www\.)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)*'
        urls = re.findall(pattern, text)
        return [url[0] + url[1] + url[2] if url[0] or url[1] else 'https://' + url[2] for url in urls]

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        '''从文本中提取目标路径'''
        pattern = r'(https?://)?(www\.)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(/[A-Za-z0-9_.-]+)*'
        match = re.search(pattern, text)
        if match:
            url = match.group(0)
            path = url.split('github.com/')[-1]
            return path.split('/')[-1] if path else None
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        '''从URL推断仓库名称'''
        pattern = r'github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)'
        match = re.search(pattern, url)
        if match:
            return match.group(2)
        raise ValueError("Invalid GitHub URL")
