
import re
from typing import List


class URLExtractor:

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        if 'arxiv.org/abs/' in url:
            return url.replace('arxiv.org/abs/', 'arxiv.org/pdf/')
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        url_pattern = re.compile(r'https?://[^\s]+')
        return url_pattern.findall(text)

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        return url.split('/')[-1]
