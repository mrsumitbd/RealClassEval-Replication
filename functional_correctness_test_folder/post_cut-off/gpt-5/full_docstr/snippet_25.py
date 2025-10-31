from typing import List
import re
from urllib.parse import urlparse, unquote


class URLExtractor:
    '''URL提取器'''

    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        '''将arXiv网页链接转换为PDF下载链接'''
        if not isinstance(url, str) or not url:
            return url
        s = url.strip()

        # Normalize scheme and host case for checking
        parsed = urlparse(s)
        host = (parsed.netloc or "").lower()
        path = parsed.path or ""

        # If already a direct .pdf link on arxiv, return as-is
        if host.endswith("arxiv.org") and path.startswith("/pdf/") and path.endswith(".pdf"):
            return s

        # Handle /abs/<id> -> /pdf/<id>.pdf
        m = re.match(r"^/abs/([^?#]+)$", path)
        if host.endswith("arxiv.org") and m:
            paper_id = m.group(1)
            paper_id = paper_id.strip("/")
            if paper_id.endswith(".pdf"):
                paper_id = paper_id[:-4]
            return f"https://arxiv.org/pdf/{paper_id}.pdf"

        # Handle /format/<id> -> /pdf/<id>.pdf
        m = re.match(r"^/format/([^?#/]+)$", path)
        if host.endswith("arxiv.org") and m:
            paper_id = m.group(1)
            return f"https://arxiv.org/pdf/{paper_id}.pdf"

        # Handle direct identifier given as URL-like "arXiv:<id>" or "https://arxiv.org/abs/<id>#..." with fragments/queries
        if s.lower().startswith("arxiv:"):
            paper_id = s.split(":", 1)[1].strip()
            paper_id = re.sub(r"\s+", "", paper_id)
            if paper_id:
                return f"https://arxiv.org/pdf/{paper_id}.pdf"

        # If it's arxiv host but different path, try to extract an arxiv id from path
        if host.endswith("arxiv.org"):
            m = re.search(r"/(abs|pdf|format)/([^/?#]+)", path)
            if m:
                paper_id = m.group(2)
                paper_id = paper_id.rstrip(".pdf")
                return f"https://arxiv.org/pdf/{paper_id}.pdf"

        return s

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        '''从文本中提取URL'''
        if not isinstance(text, str) or not text:
            return []

        # Regex to capture http/https/ftp URLs, avoiding trailing punctuation
        pattern = re.compile(r"""
            \b
            (                               # capture the whole URL
              (?:(?:https?|ftp)://)         # scheme
              [^\s<>"'(){}\[\]]+            # the body (no spaces or brackets/quotes)
              (?:
                \([^\s<>"']*\)              # allow balanced parentheses content
                |                           # or
                [^\s<>"'(){}\[\]]           # normal chars
              )*
            )
        """, re.VERBOSE | re.IGNORECASE)

        candidates = pattern.findall(text)

        # Clean typical trailing punctuation and surrounding brackets
        def clean(u: str) -> str:
            u = u.strip()
            # Strip surrounding brackets from markdown-like or sentence punctuation
            # but keep valid URL chars
            trailing = '.,;:!?)]}>"\''
            leading = '([{"\''
            if u and u[0] in leading and u[-1:] in trailing:
                u = u[1:-1]
            # Remove trailing punctuation that is unlikely part of URL
            while u and u[-1] in trailing:
                # Keep .pdf, .html etc: only strip if punctuation not part of extension
                if u.lower().endswith((".pdf", ".html", ".htm", ".png", ".jpg", ".jpeg", ".gif", ".svg", ".zip", ".tar.gz", ".tgz", ".bz2", ".xz")):
                    break
                u = u[:-1]
            return u

        seen = set()
        result = []
        for c in candidates:
            url = clean(c)
            if not url:
                continue
            if url not in seen:
                seen.add(url)
                result.append(url)
        return result

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        '''从URL推断文件名'''
        if not isinstance(url, str) or not url.strip():
            return "download"
        s = url.strip()

        # Special handling for arXiv
        arxiv_pdf = URLExtractor.convert_arxiv_url(s)
        parsed = urlparse(arxiv_pdf)
        path = parsed.path or ""
        filename = ""

        # Try to use last segment of path
        if path and path != "/":
            filename = path.rstrip("/").split("/")[-1]

        # If arxiv /pdf/<id> without .pdf, append
        if parsed.netloc.lower().endswith("arxiv.org"):
            if parsed.path.startswith("/pdf/"):
                # ensure .pdf
                base = parsed.path.split("/pdf/", 1)[-1].strip("/")
                if not base.endswith(".pdf"):
                    base += ".pdf"
                filename = base

        # Strip query/fragment artifacts from filename-like strings (some CDNs append params)
        if filename:
            # Remove fragment indicator if accidentally within the last segment
            filename = filename.split("#", 1)[0]
            filename = filename.split("?", 1)[0]

        # If no filename derived, fabricate from host
        if not filename:
            host = (parsed.netloc or "file").split(":")[0]
            if not host:
                host = "download"
            filename = host

        # If still no extension, infer .html for typical web pages
        if "." not in filename.split("/")[-1]:
            # If it looks like an arXiv ID, append .pdf; else .html
            if parsed.netloc.lower().endswith("arxiv.org"):
                filename += ".pdf"
            else:
                filename += ".html"

        # Decode percent-encoding
        filename = unquote(filename)

        # Basic sanitization: remove characters not suitable for filenames
        filename = re.sub(r"[\\/:*?\"<>|]", "_", filename).strip()
        if not filename:
            filename = "download"
        return filename
