
import re
from typing import List


class URLExtractor:
    '''URL提取器'''
    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        if 'arxiv.org/abs/' in url:
            return url.replace('arxiv.org/abs/', 'arxiv.org/pdf/') + '.pdf'
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
        urls = re.findall(url_pattern, text)
        return urls

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        filename = url.split('/')[-1]
        if '?' in filename:
            filename = filename.split('?')[0]
        return filename
