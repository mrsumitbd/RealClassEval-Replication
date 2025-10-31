import re
from typing import List
from urllib.parse import urlparse, unquote, parse_qs


class URLExtractor:
    '''URL提取器'''

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        # arXiv abs/xxxx.xxxx or pdf/xxxx.xxxx.pdf or legacy id
        # Examples:
        # https://arxiv.org/abs/1234.5678 -> https://arxiv.org/pdf/1234.5678.pdf
        # https://arxiv.org/abs/math/0301234 -> https://arxiv.org/pdf/math/0301234.pdf
        # https://arxiv.org/pdf/1234.5678.pdf -> https://arxiv.org/pdf/1234.5678.pdf
        # https://arxiv.org/ftp/arxiv/papers/1234/12345678.pdf -> unchanged
        parsed = urlparse(url)
        if parsed.netloc not in ("arxiv.org", "www.arxiv.org"):
            return url
        path = parsed.path
        if path.startswith("/abs/"):
            paper_id = path[len("/abs/"):]
            return f"https://arxiv.org/pdf/{paper_id}.pdf"
        elif path.startswith("/pdf/") and path.endswith(".pdf"):
            return url
        else:
            return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        # Simple regex for URLs
        url_pattern = re.compile(
            r'(https?://[^\s<>"\'\]\)}]+)'
        )
        return url_pattern.findall(text)

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        parsed = urlparse(url)
        path = parsed.path
        filename = path.rstrip('/').split('/')[-1]
        if not filename:
            # Try to get from query string, e.g., ?file=xxx.pdf
            qs = parse_qs(parsed.query)
            for key in ['file', 'filename', 'name', 'download']:
                if key in qs and qs[key]:
                    return unquote(qs[key][0])
            return "downloaded.file"
        return unquote(filename)
