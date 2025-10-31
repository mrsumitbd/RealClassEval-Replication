import re
import posixpath
from typing import List, Optional
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
        except Exception:
            return url

        host = (parsed.netloc or '').lower()
        if 'arxiv.org' not in host:
            return url

        path = parsed.path or ''
        if path.startswith('/abs/'):
            paper_id = path[len('/abs/'):].strip('/')
            if not paper_id:
                return url
            return f'https://arxiv.org/pdf/{paper_id}.pdf'
        if path.startswith('/pdf/'):
            # Ensure .pdf suffix
            if not path.endswith('.pdf'):
                path = f'{path}.pdf'
            # Build normalized URL with https and no query/fragment
            return urlunparse(('https', 'arxiv.org', path, '', '', ''))
        # Other arxiv paths leave unchanged
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        if not text:
            return []
        pattern = re.compile(
            r'((?:https?://|www\.)[^\s<>"\'\]\)}]+)', re.IGNORECASE)
        candidates = pattern.findall(text)

        trailing_punct = '.,;:!?)]}\'"'
        leading_punct = '([\'"'

        urls: List[str] = []
        seen = set()
        for cand in candidates:
            url = cand.strip()

            # Trim leading punctuation
            while url and url[0] in leading_punct:
                url = url[1:]
            # Trim trailing punctuation commonly attached to URLs in prose
            while url and url[-1] in trailing_punct:
                url = url[:-1]

            if not url:
                continue

            # Normalize www. to http:// if scheme missing
            if url.lower().startswith('www.'):
                url = 'http://' + url

            # Remove trailing unmatched parenthesis if likely extraneous
            # e.g., http://example.com/foo)
            open_paren = url.count('(')
            close_paren = url.count(')')
            while close_paren > open_paren and url.endswith(')'):
                url = url[:-1]
                close_paren -= 1

            if url not in seen:
                seen.add(url)
                urls.append(url)

        return urls

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        default_name = 'download'
        if not url:
            return default_name

        try:
            parsed = urlparse(url)
        except Exception:
            return default_name

        # Prefer filename-like query parameters
        query = parse_qs(parsed.query or '')
        filename_keys = ['filename', 'file',
                         'name', 'download', 'attname', 'title']
        candidate: Optional[str] = None
        for key in filename_keys:
            vals = query.get(key)
            if vals:
                candidate = vals[0]
                break

        # If no filename from query, use path basename
        if not candidate:
            path = parsed.path or ''
            base = posixpath.basename(path.rstrip('/'))
            candidate = base if base else parsed.netloc or default_name

        candidate = unquote(candidate) if candidate else default_name

        # If still empty after unquoting
        if not candidate:
            candidate = default_name

        # If name looks like a directory (no dot and came from path ending with slash), keep as-is
        # Otherwise, if it has no extension and path ended with slash or no path,
        # leave extensionless; we avoid forcing .html to keep neutral.
        # Sanitize filename
        def sanitize(name: str) -> str:
            # Remove control chars
            name = ''.join(ch for ch in name if ch >= ' ')

            # Replace invalid filesystem characters
            invalid = '<>:"/\\|?*\0'
            trans = {ord(ch): '_' for ch in invalid}
            name = name.translate(trans)

            # Strip leading/trailing dots and spaces
            name = name.strip(' .')

            # Collapse whitespace
            name = re.sub(r'\s+', '_', name)

            # Avoid empty name
            return name or default_name

        safe = sanitize(candidate)

        # If still empty, fall back
        if not safe:
            safe = default_name

        # Limit length to typical filesystem limits
        if len(safe) > 255:
            # Try to preserve extension if present
            if '.' in safe:
                root, ext = safe.rsplit('.', 1)
                max_root = max(1, 255 - len(ext) - 1)
                safe = root[:max_root] + '.' + ext
            else:
                safe = safe[:255]

        return safe
