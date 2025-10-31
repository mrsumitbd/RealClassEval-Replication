
import re
from typing import List


class URLExtractor:
    '''URL提取器'''
    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        if 'arxiv.org' in url:
            url = url.replace('abs', 'pdf')
            if not url.endswith('.pdf'):
                url += '.pdf'
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
        urls = re.findall(url_pattern, text)
        return urls

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        if not url:
            return ''
        # Remove query parameters and fragments
        clean_url = url.split('?')[0].split('#')[0]
        # Extract the last part of the URL
        filename = clean_url.split('/')[-1]
        return filename if filename else 'unnamed'
