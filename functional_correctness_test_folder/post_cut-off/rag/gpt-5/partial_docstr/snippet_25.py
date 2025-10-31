import os
import re
from typing import List
from urllib.parse import urlparse, parse_qs, unquote, urlunparse


class URLExtractor:
    '''URL提取器'''

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        if not url:
            return url
        try:
            parsed = urlparse(url)
            host = (parsed.netloc or '').lower()
            if 'arxiv.org' not in host:
                return url

            path = parsed.path or ''
            # Already a PDF link
            if path.startswith('/pdf/'):
                pdf_path = path
                if not pdf_path.endswith('.pdf'):
                    pdf_path = pdf_path.rstrip('/') + '.pdf'
                return urlunparse((parsed.scheme or 'https', 'arxiv.org', pdf_path, '', '', ''))

            # Convert /abs/<id> -> /pdf/<id>.pdf
            if path.startswith('/abs/'):
                paper_id = path.split('/abs/', 1)[1].strip('/')
                if not paper_id:
                    return url
                pdf_path = f'/pdf/{paper_id}.pdf'
                return urlunparse((parsed.scheme or 'https', 'arxiv.org', pdf_path, '', '', ''))

            return url
        except Exception:
            return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        if not text:
            return []

        # Match http(s)/ftp URLs; stop at whitespace or common closing punctuation
        pattern = re.compile(
            r'(https?://[^\s<>"\'\)\]\}，。；：！、]+|ftp://[^\s<>"\'\)\]\}，。；：！、]+)', re.IGNORECASE)
        candidates = pattern.findall(text)

        trailing_punct = '.,;:!?)]}>’”\'"、，。；：！）》】'
        cleaned: List[str] = []
        seen = set()
        for u in candidates:
            url = u.strip()
            # Strip trailing punctuation safely
            while url and url[-1] in trailing_punct:
                url = url[:-1]
            # Strip surrounding <...> if present
            if url.startswith('<') and url.endswith('>'):
                url = url[1:-1]
            if url and url not in seen:
                cleaned.append(url)
                seen.add(url)
        return cleaned

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        if not url:
            return 'download'

        # Normalize potential arXiv links to PDF
        url = URLExtractor.convert_arxiv_url(url)

        try:
            parsed = urlparse(url)
            path = unquote(parsed.path or '')
            name = os.path.basename(path)

            # If path doesn't provide a filename, inspect common query params
            if not name or name in ('/', '.', ''):
                qs = parse_qs(parsed.query or '')
                for key in ('filename', 'file', 'name', 'download', 'attachment'):
                    if key in qs and qs[key]:
                        candidate = qs[key][0]
                        candidate = os.path.basename(unquote(candidate))
                        if candidate:
                            name = candidate
                            break

            # If still no name, fallback to host-based
            if not name or name in ('/', '.', ''):
                host = (parsed.netloc or 'download').split(':', 1)[0]
                safe_host = re.sub(r'[^A-Za-z0-9._-]+',
                                   '_', host) or 'download'
                return f'{safe_host}'

            # Ensure it is safe for filesystem
            safe_name = re.sub(r'[\\/:*?"<>|\r\n]+', '_', name).strip()
            safe_name = safe_name or 'download'

            return safe_name
        except Exception:
            return 'download'
