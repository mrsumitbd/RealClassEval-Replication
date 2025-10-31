
import re
from typing import List


class URLExtractor:

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        arxiv_pattern = re.compile(
            r'arxiv\.org/(abs|pdf)/(\d+\.\d+)(v\d+)?(\.pdf)?')
        match = arxiv_pattern.search(url)
        if match:
            arxiv_id = match.group(2)
            version = match.group(3) if match.group(3) else ''
            return f"https://arxiv.org/pdf/{arxiv_id}{version}.pdf"
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        url_pattern = re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+')
        urls = re.findall(url_pattern, text)
        return urls

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        filename = url.split('/')[-1].split('?')[0]
        if not filename:
            filename = "untitled"
        return filename
