
import re
from typing import List
from urllib.parse import urlparse, unquote


class URLExtractor:
    '''URL提取器'''
    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        # Accepts both https://arxiv.org/abs/xxxx and https://arxiv.org/pdf/xxxx.pdf
        # Converts to https://arxiv.org/pdf/xxxx.pdf
        m = re.match(r'(https?://arxiv\.org/)(abs|pdf)/([^\s/?#]+)', url)
        if m:
            paper_id = m.group(3)
            if not paper_id.endswith('.pdf'):
                paper_id += '.pdf'
            return f'https://arxiv.org/pdf/{paper_id}'
        # If already a direct PDF link
        m2 = re.match(r'(https?://arxiv\.org/)([^\s?#]+\.pdf)', url)
        if m2:
            return url
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        # Simple regex for URLs
        url_pattern = re.compile(
            r'(https?://[^\s"\'<>]+)'
        )
        return url_pattern.findall(text)

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        parsed = urlparse(url)
        path = parsed.path
        if path.endswith('/'):
            path = path[:-1]
        filename = path.split('/')[-1]
        if not filename:
            filename = 'index.html'
        filename = unquote(filename)
        return filename
