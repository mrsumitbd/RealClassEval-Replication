
import re
from typing import List
from urllib.parse import urlparse, unquote


class URLExtractor:

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        """
        Converts an arXiv abstract or PDF URL to the canonical PDF download URL.
        """
        # Remove any trailing whitespace
        url = url.strip()
        # Patterns:
        # https://arxiv.org/abs/xxxx.xxxx
        # https://arxiv.org/pdf/xxxx.xxxx.pdf
        # https://arxiv.org/abs/xxxx.xxxxvN
        # https://arxiv.org/pdf/xxxx.xxxxvN.pdf
        abs_pattern = r'https?://arxiv\.org/abs/([0-9]+\.[0-9]+(v[0-9]+)?)'
        pdf_pattern = r'https?://arxiv\.org/pdf/([0-9]+\.[0-9]+(v[0-9]+)?)\.pdf'
        m = re.match(abs_pattern, url)
        if m:
            arxiv_id = m.group(1)
            return f'https://arxiv.org/pdf/{arxiv_id}.pdf'
        m = re.match(pdf_pattern, url)
        if m:
            arxiv_id = m.group(1)
            return f'https://arxiv.org/pdf/{arxiv_id}.pdf'
        # If not an arXiv URL, return as is
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """
        Extracts all URLs from the given text.
        """
        # Regex for URLs (http, https, ftp)
        url_pattern = r'(https?://[^\s<>"\'\)\]]+|ftp://[^\s<>"\'\)\]]+)'
        urls = re.findall(url_pattern, text)
        # Remove trailing punctuation
        cleaned_urls = [u.rstrip('.,;:!?)]}') for u in urls]
        return cleaned_urls

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        """
        Infers a filename from the URL.
        """
        parsed = urlparse(url)
        path = parsed.path
        if path.endswith('/'):
            path = path[:-1]
        filename = path.split('/')[-1]
        if not filename:
            # If no filename, use domain
            filename = parsed.netloc
        filename = unquote(filename)
        # If arXiv, use arXiv id.pdf
        arxiv_pdf_pattern = r'https?://arxiv\.org/pdf/([0-9]+\.[0-9]+(v[0-9]+)?)\.pdf'
        arxiv_abs_pattern = r'https?://arxiv\.org/abs/([0-9]+\.[0-9]+(v[0-9]+)?)'
        m = re.match(arxiv_pdf_pattern, url)
        if m:
            return f"{m.group(1)}.pdf"
        m = re.match(arxiv_abs_pattern, url)
        if m:
            return f"{m.group(1)}.pdf"
        # If filename is empty, fallback to domain
        if not filename:
            filename = parsed.netloc
        return filename
