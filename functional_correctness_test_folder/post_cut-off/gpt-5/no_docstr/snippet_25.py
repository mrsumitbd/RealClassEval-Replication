from typing import List
import re
from urllib.parse import urlparse, parse_qs, unquote


class URLExtractor:
    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        if not url:
            return url
        try:
            p = urlparse(url)
        except Exception:
            return url

        host = (p.netloc or "").lower()
        if host.endswith("arxiv.org"):
            path = p.path or ""
            # Normalize multiple slashes
            path = re.sub(r"/{2,}", "/", path)

            def build_pdf_url(arxiv_id: str) -> str:
                arxiv_id = arxiv_id.strip().strip("/")
                arxiv_id = re.sub(r"\.pdf$", "", arxiv_id, flags=re.IGNORECASE)
                if not arxiv_id:
                    return url
                return f"https://arxiv.org/pdf/{arxiv_id}.pdf"

            if path.startswith("/abs/"):
                arxiv_id = path[len("/abs/"):]
                return build_pdf_url(arxiv_id)
            if path.startswith("/pdf/"):
                id_part = path[len("/pdf/"):]
                id_part = id_part.strip("/")
                id_part = re.sub(r"\.pdf$", "", id_part, flags=re.IGNORECASE)
                return build_pdf_url(id_part)

        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        if not text:
            return []
        # Basic URL regex capturing http(s):// or www.
        pattern = re.compile(
            r"(?P<url>(?:https?://|www\.)[^\s<>\[\]{}\"']+)", re.IGNORECASE)
        results: List[str] = []

        def clean_trailing_punct(s: str) -> str:
            # Remove trailing punctuation commonly adjacent to URLs in prose
            trailing = '.,);:!?"\'»›]}'
            opening = "([{«‹"
            closing = ")]}"
            # Balance parentheses: keep closing only if there's an opening
            while s and s[-1] in trailing:
                if s[-1] in ")]}":
                    # If more closings than openings, drop one
                    for o, c in zip(opening, closing):
                        pass
                    # Rough balance check for ')' only
                    if s[-1] == ")":
                        if s.count("(") < s.count(")"):
                            s = s[:-1]
                        else:
                            break
                    else:
                        s = s[:-1]
                else:
                    s = s[:-1]
            # Strip unmatched closing angle bracket
            if s.endswith(">"):
                s = s[:-1]
            return s

        for m in pattern.finditer(text):
            u = m.group("url")
            u = clean_trailing_punct(u)
            if u.lower().startswith("www."):
                u = "http://" + u
            results.append(u)
        return results

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        if not url:
            return "download"
        try:
            # Normalize arXiv URLs to a consistent PDF link
            normalized = URLExtractor.convert_arxiv_url(url)
            p = urlparse(normalized)
        except Exception:
            return "download"

        host = (p.netloc or "").strip().lower()
        path = unquote(p.path or "")
        query = parse_qs(p.query or "")

        # If arXiv, derive filename from ID and ensure .pdf
        if host.endswith("arxiv.org"):
            arxiv_id = ""
            if path.startswith("/pdf/"):
                arxiv_id = re.sub(r"^/pdf/", "", path).strip("/")
                arxiv_id = re.sub(r"\.pdf$", "", arxiv_id, flags=re.IGNORECASE)
            elif path.startswith("/abs/"):
                arxiv_id = path[len("/abs/"):].strip("/")
            if arxiv_id:
                safe_id = arxiv_id.replace("/", "_")
                return f"{safe_id}.pdf"

        # Try basename from path
        filename = ""
        if path and path != "/":
            # Get last segment ignoring trailing slash
            segs = [s for s in path.split("/") if s]
            if segs:
                filename = segs[-1]

        # Some services provide filename via query parameters
        if not filename:
            for key in ("filename", "file", "name", "attachment", "download"):
                if key in query and query[key]:
                    candidate = query[key][0]
                    if candidate:
                        filename = unquote(candidate)
                        break

        # Fallback to host if still empty
        if not filename:
            filename = host or "download"

        # Sanitize filename for common filesystems
        filename = filename.strip().strip(".")
        # Remove URL fragments if accidentally present
        filename = filename.split("#", 1)[0]
        # Avoid query artifacts
        filename = filename.split("?", 1)[0]
        # Replace path separators and forbidden characters
        filename = filename.replace("\\", "_").replace(
            "/", "_").replace(":", "-")
        filename = re.sub(r'[<>|"*?]', "_", filename)

        # If filename looks like a directory (no dot), keep as is
        # but avoid empty string
        if not filename:
            filename = "download"

        return filename
