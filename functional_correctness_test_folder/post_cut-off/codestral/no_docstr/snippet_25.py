
import re
from typing import List


class URLExtractor:

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        pattern = r'https?://arxiv\.org/(?:abs|pdf)/(\d+\.\d+)'
        match = re.search(pattern, url)
        if match:
            return f'https://arxiv.org/pdf/{match.group(1)}.pdf'
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[/\w .-]*/?'
        urls = re.findall(pattern, text)
        return [cls.convert_arxiv_url(url) for url in urls]

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        pattern = r'/([^/]+\.\w+)(?:\?|$)'
        match = re.search(pattern, url)
        if match:
            return match.group(1)
        return 'file'
