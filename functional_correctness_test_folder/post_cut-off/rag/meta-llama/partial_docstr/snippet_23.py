
import re
from typing import List, Optional


class GitHubURLExtractor:
    """
    提取GitHub URL的工具类
    """

    @staticmethod
    def extract_github_urls(text: str) -> List[str]:
        """
        从文本中提取GitHub URLs

        :param text: 要提取URL的文本
        :return: 提取的GitHub URL列表
        """
        pattern = r'(https://github\.com/[^\s]+)'
        return re.findall(pattern, text)

    @staticmethod
    def extract_target_path(text: str) -> Optional[str]:
        """
        从文本中提取目标路径

        :param text: 要提取目标路径的文本
        :return: 提取的目标路径，如果没有找到则返回None
        """
        pattern = r'#L(\d+)-L(\d+)'
        match = re.search(pattern, text)
        if match:
            start_line, end_line = match.groups()
            return f'L{start_line}-L{end_line}'
        return None

    @staticmethod
    def infer_repo_name(url: str) -> str:
        """
        从URL推断仓库名称

        :param url: GitHub URL
        :return: 推断出的仓库名称
        """
        pattern = r'https://github\.com/([^/]+)/([^/]+)'
        match = re.search(pattern, url)
        if match:
            owner, repo = match.groups()
            return f'{owner}/{repo}'
        return ''
