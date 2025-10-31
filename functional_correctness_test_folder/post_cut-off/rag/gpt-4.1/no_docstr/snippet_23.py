import re
from typing import List, Optional


class GitHubURLExtractor:
    '''提取GitHub URL的工具类'''

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        '''从文本中提取GitHub URLs'''
        # 匹配 https://github.com/owner/repo 或 https://github.com/owner/repo/...
        pattern = re.compile(
            r'https?://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+(?:[/?#][^\s]*)?',
            re.IGNORECASE
        )
        return pattern.findall(text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        '''从文本中提取目标路径'''
        # 假设目标路径以 "路径:"、"path:"、"target:"、"目标路径:"、"文件路径:"、"file:"、"filepath:"、"file path:" 等关键词后跟路径
        # 支持中英文冒号
        pattern = re.compile(
            r'(?:路径|path|target|目标路径|文件路径|file|filepath|file path)\s*[:：]\s*([^\s]+)',
            re.IGNORECASE
        )
        match = pattern.search(text)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        '''从URL推断仓库名称'''
        # 只提取 owner/repo
        pattern = re.compile(
            r'https?://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)',
            re.IGNORECASE
        )
        match = pattern.match(url)
        if match:
            return f"{match.group(1)}/{match.group(2)}"
        # 如果不是完整URL，尝试 owner/repo 格式
        pattern2 = re.compile(r'^([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)$')
        match2 = pattern2.match(url)
        if match2:
            return f"{match2.group(1)}/{match2.group(2)}"
        return ""
