import re
from typing import List
from urllib.parse import urlparse, unquote, parse_qs


class URLExtractor:
    '''URL提取器'''

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        # arXiv URLs can be like: https://arxiv.org/abs/xxxx.xxxx or https://arxiv.org/pdf/xxxx.xxxx.pdf
        # Convert abs to pdf
        parsed = urlparse(url)
        if parsed.netloc.endswith('arxiv.org'):
            # Handle /abs/xxxx.xxxx or /abs/xxxx.xxxxvN
            m = re.match(r'^/abs/([\w\.\-]+)$', parsed.path)
            if m:
                paper_id = m.group(1)
                return f'https://arxiv.org/pdf/{paper_id}.pdf'
            # Already a pdf link
            m2 = re.match(r'^/pdf/([\w\.\-]+)\.pdf$', parsed.path)
            if m2:
                return url
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        # Simple regex for URLs
        url_pattern = re.compile(
            r'(https?://[^\s<>"\'\]\)]+)'
        )
        return url_pattern.findall(text)

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        parsed = urlparse(url)
        path = parsed.path
        filename = path.rstrip('/').split('/')[-1]
        if not filename:
            # Try to get from query string (e.g., ?file=xxx.pdf)
            qs = parse_qs(parsed.query)
            for key in ['file', 'filename', 'name', 'download']:
                if key in qs and qs[key]:
                    return unquote(qs[key][0])
            return 'downloaded_file'
        return unquote(filename)
