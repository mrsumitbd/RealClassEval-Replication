
import re
from typing import List


class URLExtractor:
    '''URL提取器'''
    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        if 'arxiv.org' in url:
            match = re.search(r'arxiv\.org/(?:abs|pdf)/(\d+\.\d+)', url)
            if match:
                return f'https://arxiv.org/pdf/{match.group(1)}.pdf'
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        url_pattern = re.compile(
            r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w .-]*(?:\?[/\w .-]*)?(?:\#[/\w .-]*)?')
        urls = re.findall(url_pattern, text)
        return [cls.convert_arxiv_url(url) for url in urls]

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        match = re.search(r'/([^/]+\.[a-zA-Z0-9]+)(?:\?|$)', url)
        if match:
            return match.group(1)
        return 'downloaded_file'
