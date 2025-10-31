from typing import List
import re
import os
from urllib.parse import urlparse, urlunparse, parse_qs, unquote


class URLExtractor:
    '''URL提取器'''

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        try:
            parsed = urlparse(url)
        except Exception:
            return url
        netloc = (parsed.netloc or "").lower()
        if not netloc.endswith("arxiv.org") and not netloc.endswith("export.arxiv.org"):
            return url

        path = parsed.path or ""
        if path.startswith("/abs/"):
            arxiv_id = path[len("/abs/"):]
            if arxiv_id.endswith(".pdf"):
                new_path = f"/pdf/{arxiv_id}"
            else:
                new_path = f"/pdf/{arxiv_id}.pdf"
            return urlunparse((parsed.scheme or "https", parsed.netloc, new_path, "", "", parsed.fragment))
        elif path.startswith("/pdf/"):
            # Ensure .pdf suffix
            if not path.endswith(".pdf"):
                path = path + ".pdf"
            return urlunparse((parsed.scheme or "https", parsed.netloc, path, "", "", parsed.fragment))
        else:
            return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        if not text:
            return []
        # Find http/https URLs
        pattern = re.compile(r'https?://[^\s<>()"\']+')
        raw = pattern.findall(text)

        # Clean trailing punctuation commonly attached in prose
        def clean(u: str) -> str:
            u = u.strip()
            # strip trailing punctuation
            trailing = ',.;:!?)\]}›»'
            leading = '([{'  # rarely attached at start
            # balance common parentheses/brackets
            while u and u[-1] in trailing:
                # avoid stripping if it balances an earlier open bracket inside URL query/fragment
                candidate = u[:-1]
                if candidate.count('(') >= candidate.count(')') and u[-1] == ')':
                    u = candidate
                    continue
                if candidate.count('[') >= candidate.count(']') and u[-1] == ']':
                    u = candidate
                    continue
                if candidate.count('{') >= candidate.count('}') and u[-1] == '}':
                    u = candidate
                    continue
                # otherwise strip
                u = candidate
            while u and u[0] in leading:
                u = u[1:]
            return u

        cleaned = [clean(u) for u in raw if u]

        # Deduplicate preserving order
        seen = set()
        result: List[str] = []
        for u in cleaned:
            if u not in seen:
                seen.add(u)
                # Normalize arXiv URLs to direct PDF when applicable
                u = cls.convert_arxiv_url(u)
                if u not in seen:
                    seen.add(u)
                result.append(u)
        return result

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        try:
            parsed = urlparse(url)
        except Exception:
            return "download"

        path = parsed.path or ""
        base = os.path.basename(path)
        base = unquote(base)

        if not base:
            host = (parsed.netloc or "").strip()
            return host or "download"

        # If base has an extension, use it
        name, ext = os.path.splitext(base)
        if ext:
            return base

        # Try to infer from query parameters
        q = parse_qs(parsed.query or "")
        for key in ("filename", "file", "name", "response-content-disposition"):
            if key in q and q[key]:
                candidate = unquote(q[key][0])
                # try to extract filename from content-disposition-like value
                m = re.search(
                    r'filename\*?=(?:UTF-8\'\')?["\']?([^"\';]+)', candidate, re.IGNORECASE)
                if m:
                    filename = m.group(1)
                    return filename
                # else assume whole value is filename
                if "." in candidate:
                    return candidate

        # If arXiv direct PDF without extension (handled earlier to ensure .pdf), fallback
        if "arxiv.org" in (parsed.netloc or "").lower() and "/pdf/" in path:
            arxiv_id = path.rsplit("/", 1)[-1]
            if not arxiv_id.endswith(".pdf"):
                return f"{arxiv_id}.pdf"
            return arxiv_id

        return base or "download"
