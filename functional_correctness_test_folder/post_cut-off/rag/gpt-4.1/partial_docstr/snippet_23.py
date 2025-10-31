import re
from typing import List, Optional


class GitHubURLExtractor:
    '''提取GitHub URL的工具类'''

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        '''从文本中提取GitHub URLs'''
        # 匹配 http(s)://github.com/owner/repo[.git][...]
        pattern = re.compile(
            r'https?://github\.com/[\w\-\.]+/[\w\-\.]+(?:\.git)?(?:[/?#][^\s]*)?',
            re.IGNORECASE
        )
        return pattern.findall(text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        '''从文本中提取目标路径'''
        # 假设目标路径格式为: path: <some_path> 或 Path: <some_path>
        match = re.search(r'(?:path|Path)\s*:\s*([^\s]+)', text)
        if match:
            return match.group(1)
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        '''从URL推断仓库名称'''
        # 匹配 https://github.com/owner/repo(.git)?/...
        match = re.match(
            r'https?://github\.com/([\w\-\.]+)/([\w\-\.]+)',
            url,
            re.IGNORECASE
        )
        if match:
            return match.group(2)
        return ''
