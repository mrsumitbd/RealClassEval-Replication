
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
        '''从文本中提取URL'''
        url_pattern = re.compile(r'https?://[^\s]+')
        return url_pattern.findall(text)

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        return url.split('/')[-1]
