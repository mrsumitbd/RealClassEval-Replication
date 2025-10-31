
import re
from typing import List


class URLExtractor:
    '''URL提取器'''
    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        if not url:
            return url
        # Handle arXiv URLs like https://arxiv.org/abs/1234.5678 or https://arxiv.org/pdf/1234.5678
        arxiv_pattern = re.compile(r'arxiv\.org/(abs|pdf)/(\d+\.\d+)')
        match = arxiv_pattern.search(url)
        if match:
            return f"https://arxiv.org/pdf/{match.group(2)}.pdf"
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        if not text:
            return []
        url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
        urls = re.findall(url_pattern, text)
        return urls

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        if not url:
            return ""
        # Extract the last part of the URL
        filename = url.split('/')[-1]
        # Remove query parameters if any
        filename = filename.split('?')[0]
        # Remove fragments if any
        filename = filename.split('#')[0]
        return filename
