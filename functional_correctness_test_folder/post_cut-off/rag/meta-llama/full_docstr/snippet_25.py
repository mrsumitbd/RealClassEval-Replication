
from typing import List
import re
from urllib.parse import urlparse, urlunparse


class URLExtractor:
    """URL提取器"""

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        """将arXiv网页链接转换为PDF下载链接"""
        parsed_url = urlparse(url)
        if 'arxiv.org' in parsed_url.netloc:
            path_parts = parsed_url.path.split('/')
            if len(path_parts) > 2 and path_parts[1] == 'abs':
                pdf_path = '/pdf/' + path_parts[-1] + '.pdf'
                return urlunparse(('https', 'arxiv.org', pdf_path, '', '', ''))
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """从文本中提取URL"""
        url_pattern = r'(https?://[^\s]+)'
        return re.findall(url_pattern, text)

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        """从URL推断文件名"""
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.split('/')
        filename = path_parts[-1]
        if not filename:
            filename = 'unknown'
        return filename
