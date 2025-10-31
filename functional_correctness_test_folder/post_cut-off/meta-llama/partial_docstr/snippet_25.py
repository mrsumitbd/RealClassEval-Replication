
import re
from urllib.parse import urlparse
from typing import List


class URLExtractor:
    '''URL提取器'''
    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        if 'arxiv.org' not in url:
            return url
        url = url.replace('abs', 'pdf')
        if not url.endswith('.pdf'):
            url += '.pdf'
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        pattern = r'https?://[^\s]+'
        return re.findall(pattern, text)

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        parsed_url = urlparse(url)
        path = parsed_url.path
        filename = path.split('/')[-1]
        if not filename:
            filename = 'index.html'
        return filename
