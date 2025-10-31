
import re
from typing import List
from urllib.parse import urlparse, unquote


class URLExtractor:
    @staticmethod
    def convert_arxiv_url(url: str) -> str:
        """
        Convert an arXiv URL to the corresponding PDF URL.
        Handles the following patterns:
        - https://arxiv.org/abs/<id>
        - https://arxiv.org/abs/<id>?pdf=1
        - https://arxiv.org/pdf/<id>.pdf
        - https://arxiv.org/pdf/<id>
        """
        if not url:
            return url

        parsed = urlparse(url)
        if "arxiv.org" not in parsed.netloc:
            return url

        path = parsed.path
        # Handle /abs/<id> or /abs/<id>?pdf=1
        if path.startswith("/abs/"):
            arxiv_id = path[len("/abs/"):]
            # Remove any trailing slash
            arxiv_id = arxiv_id.rstrip("/")
            # Build PDF URL
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            return pdf_url

        # Handle /pdf/<id>.pdf or /pdf/<id>
        if path.startswith("/pdf/"):
            pdf_path = path[len("/pdf/"):]
            # Ensure it ends with .pdf
            if not pdf_path.endswith(".pdf"):
                pdf_path = f"{pdf_path}.pdf"
            return f"https://arxiv.org/pdf/{pdf_path}"

        # If the URL already looks like a PDF, return it unchanged
        return url

    @classmethod
    def extract_urls(cls, text: str) -> List[str]:
        """
        Extract all URLs from the given text.
        Returns a list of URLs in the order they appear.
        """
        if not text:
            return []

        # Regex to match http/https URLs
        url_pattern = re.compile(
            r"""
            (?P<url>
                https?://
                [^\s<>"'()\[\]]+
            )
            """,
            re.VERBOSE | re.IGNORECASE,
        )
        return [match.group("url") for match in url_pattern.finditer(text)]

    @staticmethod
    def infer_filename_from_url(url: str) -> str:
        """
        Infer a filename from a URL.
        Uses the last path component, stripping query parameters and fragments.
        If the path ends with a slash or is empty, falls back to the netloc.
        """
        if not url:
            return "download"

        parsed = urlparse(url)
        path = parsed.path

        # Remove trailing slash
        if path.endswith("/"):
            path = path.rstrip("/")

        # Get the last segment
        filename = path.split("/")[-1] if path else ""

        # If the filename is empty, use the netloc
        if not filename:
            filename = parsed.netloc

        # Strip query and fragment
        filename = unquote(filename.split("?")[0].split("#")[0])

        # Fallback if still empty
        if not filename:
            filename = "download"

        return filename
