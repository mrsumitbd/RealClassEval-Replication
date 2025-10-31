
import re
from typing import List
from urllib.parse import urlparse, unquote


class URLExtractor:
    '''URL提取器'''
    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        # Normalize URL
        url = url.strip()
        # Patterns:
        # https://arxiv.org/abs/xxxx.xxxx
        # https://arxiv.org/pdf/xxxx.xxxx.pdf
        # https://arxiv.org/abs/xxxx.xxxxvN
        # https://arxiv.org/pdf/xxxx.xxxxvN.pdf
        m = re.match(
            r'https?://arxiv\.org/(abs|pdf)/([0-9]+\.[0-9]+(v[0-9]+)?)(\.pdf)?', url)
        if m:
            arxiv_id = m.group(2)
            return f'https://arxiv.org/pdf/{arxiv_id}.pdf'
        # Also support legacy arXiv IDs: arxiv.org/abs/math/0301234
        m2 = re.match(
            r'https?://arxiv\.org/(abs|pdf)/([a-z\-]+/\d{7}(v\d+)?)(\.pdf)?', url)
        if m2:
            arxiv_id = m2.group(2)
            return f'https://arxiv.org/pdf/{arxiv_id}.pdf'
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        # Simple regex for URLs
        url_pattern = re.compile(
            r'(https?://[^\s<>"\'\]\)}]+)'
        )
        urls = url_pattern.findall(text)
        # Remove trailing punctuation
        cleaned_urls = [u.rstrip('.,;:!?)]}\'"') for u in urls]
        return cleaned_urls

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        parsed = urlparse(url)
        path = parsed.path
        if not path or path.endswith('/'):
            return 'index.html'
        filename = path.split('/')[-1]
        if not filename:
            return 'index.html'
        filename = unquote(filename)
        return filename
