import re
from typing import List
from urllib.parse import urlparse, urlunparse, parse_qs, unquote
import posixpath


class URLExtractor:
    '''URL提取器'''

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        if not url:
            return url
        try:
            parsed = urlparse(url if re.match(
                r'^[a-z]+://', url, re.I) else f'https://{url}')
            host = (parsed.netloc or '').lower()
            path = parsed.path or ''
            if not host.endswith('arxiv.org'):
                return url

            # Already a direct PDF
            if path.startswith('/pdf/'):
                new_path = path if path.endswith('.pdf') else f'{path}.pdf'
                return urlunparse(('https', 'arxiv.org', new_path, '', '', ''))

            # Convert from /abs/... or /format/... to /pdf/... .pdf
            for prefix in ('/abs/', '/format/'):
                if path.startswith(prefix):
                    arxiv_id = path[len(prefix):].strip('/')
                    if arxiv_id.lower().endswith('.pdf'):
                        arxiv_id = arxiv_id[:-4]
                    new_path = f'/pdf/{arxiv_id}.pdf'
                    return urlunparse(('https', 'arxiv.org', new_path, '', '', ''))

            # Other arxiv paths: try best-effort if looks like an arxiv id
            m = re.search(r'/([0-9]{4}\.[0-9]{4,5}(v[0-9]+)?)', path)
            if m:
                arxiv_id = m.group(1)
                new_path = f'/pdf/{arxiv_id}.pdf'
                return urlunparse(('https', 'arxiv.org', new_path, '', '', ''))
        except Exception:
            pass
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        if not text:
            return []
        # Basic URL pattern capturing http, https, ftp, and www-prefixed URLs
        url_pattern = re.compile(
            r'(?i)\b((?:https?://|ftp://|www\.)[^\s<>"\'\)\]]+)')
        candidates = [m.group(1) for m in url_pattern.finditer(text)]

        def strip_trailing_punct(u: str) -> str:
            # Remove common trailing punctuation that often attaches to URLs in text
            while u and u[-1] in '.,;:!?)]}>"\'':
                if u[-1] == ')':
                    # Keep closing ')' if parentheses are balanced or tilted towards '('
                    if u.count('(') >= u.count(')'):
                        break
                u = u[:-1]
            return u

        results: List[str] = []
        seen = set()
        for c in candidates:
            u = strip_trailing_punct(c)
            if u.lower().startswith('www.'):
                u = 'http://' + u
            if u not in seen:
                seen.add(u)
                results.append(u)
        return results

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        default_name = 'downloaded_file'
        if not url:
            return default_name
        try:
            parsed = urlparse(url if re.match(
                r'^[a-z]+://', url, re.I) else f'https://{url}')
            host = (parsed.netloc or '').lower()
            path = parsed.path or ''
            qs = parse_qs(parsed.query or '')

            # Try from query parameters that frequently carry filename
            candidate_keys = ['filename', 'file', 'name', 'title', 'attname']
            for key in candidate_keys:
                if key in qs and qs[key]:
                    cand = qs[key][0]
                    cand = unquote(cand)
                    if cand:
                        name = cand
                        break
            else:
                # Content-Disposition in query (e.g., response-content-disposition=attachment;filename="x.pdf")
                cd_list = qs.get(
                    'response-content-disposition') or qs.get('content-disposition') or []
                name = ''
                if cd_list:
                    cd = unquote(cd_list[0])
                    m = re.search(
                        r'filename\*?=(?:UTF-8\'\')?"?([^\";]+)"?', cd, flags=re.I)
                    if m:
                        name = m.group(1)

            # Special handling for Google Drive share links: /file/d/<ID>/view
            if not name and host.endswith('google.com'):
                parts = [p for p in path.split('/') if p]
                if len(parts) >= 3 and parts[0] == 'file' and parts[1] == 'd':
                    file_id = parts[2]
                    name = file_id or ''

            # Fallback to path basename
            if not name:
                base = posixpath.basename(path)
                # If last path part is generic action keyword, fallback to previous part if possible
                if base in ('', 'view', 'edit', 'download', 'blob'):
                    parts = [p for p in path.split('/') if p]
                    if parts:
                        base = parts[-1]
                        if base in ('view', 'edit', 'download', 'blob') and len(parts) >= 2:
                            base = parts[-2]
                name = unquote(base)

            # Special-case arXiv: ensure .pdf if possible
            if host.endswith('arxiv.org'):
                # /pdf/<id>.pdf or /abs/<id>
                m_pdf = re.match(r'^/pdf/([^/]+)(?:\.pdf)?$', path)
                m_abs = re.match(r'^/abs/([^/]+)$', path)
                if m_pdf:
                    name = f"{m_pdf.group(1)}.pdf"
                elif m_abs:
                    name = f"{m_abs.group(1)}.pdf"

            # If still empty, use host
            if not name:
                name = host or default_name

            # If name has no extension and query suggests a format
            if '.' not in name:
                # Heuristic: if arXiv or query hints at pdf
                if host.endswith('arxiv.org') or any(k in (parsed.query or '').lower() for k in ('format=pdf', 'pdf=1')):
                    name += '.pdf'

            # Sanitize filename
            name = name.strip().strip('"\'')

            # Remove illegal filesystem characters
            name = re.sub(r'[\\/:*?"<>|]+', '_', name)
            # Remove control characters
            name = re.sub(r'[\x00-\x1f\x7f]+', '', name)
            # Limit length
            if len(name) > 255:
                # Try to preserve extension
                m = re.match(r'^(.*?)(\.[A-Za-z0-9]{1,8})$', name)
                if m:
                    stem, ext = m.groups()
                    name = (stem[: max(1, 255 - len(ext))]) + ext
                else:
                    name = name[:255]

            if not name:
                name = default_name
            return name
        except Exception:
            return default_name
