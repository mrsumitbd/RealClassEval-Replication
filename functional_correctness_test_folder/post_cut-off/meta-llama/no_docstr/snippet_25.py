
import re
from urllib.parse import urlparse
from typing import List


class URLExtractor:

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        """Converts arxiv url to pdf url"""
        if 'arxiv.org' not in url:
            return url

        # Check if the url is already in pdf format
        if 'pdf' in url:
            return url

        # Extract the arxiv id from the url
        arxiv_id = re.search(r'arxiv\.org\/abs\/([^\/]+)', url)
        if arxiv_id:
            arxiv_id = arxiv_id.group(1)
            return f'https://arxiv.org/pdf/{arxiv_id}.pdf'

        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """Extracts urls from a given text"""
        url_pattern = r'https?://\S+'
        return re.findall(url_pattern, text)

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        """Infers filename from a given url"""
        parsed_url = urlparse(url)
        path = parsed_url.path
        filename = path.split('/')[-1]

        # If the filename is empty, use the last part of the netloc
        if not filename:
            filename = parsed_url.netloc.split('.')[-2] + '.html'

        # If the filename does not have an extension, add .html
        if '.' not in filename:
            filename += '.html'

        return filename
