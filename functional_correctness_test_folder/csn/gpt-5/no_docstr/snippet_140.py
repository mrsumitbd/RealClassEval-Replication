
import re
import time
from html import unescape
from html.parser import HTMLParser
from typing import Dict, Optional


class AbstractHtmlConverter:
    class _TextExtractor(HTMLParser):
        def __init__(self) -> None:
            super().__init__(convert_charrefs=False)
            self._parts = []
            self._in_ignorable = 0  # counts nested script/style/svg/math elements
            self._last_was_space = False
            self._last_char: Optional[str] = None
            self._list_indent = 0

        def handle_starttag(self, tag, attrs):
            t = tag.lower()
            if t in ("script", "style", "svg", "math"):
                self._in_ignorable += 1
                return

            if t in ("br",):
                self._newline()
            elif t in ("p", "div", "section", "article", "header", "footer", "aside", "main", "figure"):
                self._block_break()
            elif t in ("h1", "h2", "h3", "h4", "h5", "h6"):
                self._block_break()
            elif t in ("ul", "ol"):
                self._block_break()
            elif t == "li":
                self._block_break()
                self._emit("• ")
                self._list_indent += 1
            elif t in ("tr",):
                self._block_break()
            elif t in ("td", "th"):
                self._emit("\t")

        def handle_endtag(self, tag):
            t = tag.lower()
            if t in ("script", "style", "svg", "math"):
                if self._in_ignorable > 0:
                    self._in_ignorable -= 1
                return

            if t in ("p", "div", "section", "article", "header", "footer", "aside", "main", "figure"):
                self._block_break()
            elif t in ("h1", "h2", "h3", "h4", "h5", "h6"):
                self._block_break()
            elif t in ("ul", "ol"):
                self._block_break()
            elif t == "li":
                self._list_indent = max(0, self._list_indent - 1)
                self._newline()
            elif t in ("tr",):
                self._newline()
            elif t in ("td", "th"):
                self._emit("\t")

        def handle_data(self, data):
            if self._in_ignorable:
                return
            if not data:
                return
            text = unescape(data)
            # Normalize internal whitespace to single spaces but preserve newlines if present
            # Split by lines to keep newlines inserted by tags meaningful
            for chunk in re.split(r"(\r?\n)", text):
                if chunk in ("\n", "\r\n"):
                    self._newline()
                else:
                    self._emit(self._normalize_spaces(chunk))

        def handle_entityref(self, name):
            if self._in_ignorable:
                return
            self._emit(unescape(f"&{name};"))

        def handle_charref(self, name):
            if self._in_ignorable:
                return
            self._emit(unescape(f"&#{name};"))

        def _emit(self, s: str):
            if not s:
                return
            # Collapse spaces, avoid duplicating spaces around boundaries
            for ch in s:
                if ch == "\n":
                    self._newline()
                    continue
                if ch.isspace():
                    if not self._last_was_space and self._last_char not in (None, "\n"):
                        self._parts.append(" ")
                        self._last_char = " "
                    self._last_was_space = True
                else:
                    self._parts.append(ch)
                    self._last_was_space = False
                    self._last_char = ch

        def _normalize_spaces(self, s: str) -> str:
            return re.sub(r"[ \t\f\v]+", " ", s)

        def _newline(self):
            if self._parts and self._parts[-1] != "\n":
                self._parts.append("\n")
                self._last_char = "\n"
                self._last_was_space = False

        def _block_break(self):
            # Ensure a blank line between blocks
            if not self._parts:
                return
            # If last char isn't a newline, add one
            if self._parts[-1] != "\n":
                self._parts.append("\n")
            # Ensure exactly one blank line (two newlines)
            if len(self._parts) >= 2 and (self._parts[-2] != "\n"):
                self._parts.append("\n")
            self._last_char = "\n"
            self._last_was_space = False

        def text(self) -> str:
            out = "".join(self._parts)
            # Trim trailing spaces on each line
            out = "\n".join(line.rstrip() for line in out.splitlines())
            # Collapse more than two consecutive newlines into exactly two
            out = re.sub(r"\n{3,}", "\n\n", out)
            return out.strip()

    def get_text(self, html: str) -> str:
        parser = self._TextExtractor()
        try:
            parser.feed(html or "")
            parser.close()
        except Exception:
            # Best-effort fallback: strip tags with a regex and unescape entities
            raw = re.sub(r"(?is)<(script|style|svg|math).*?</\1>",
                         " ", html or "")
            raw = re.sub(r"(?s)<br\s*/?>", "\n", raw, flags=re.I)
            raw = re.sub(
                r"(?is)</?(p|div|section|article|header|footer|aside|main|h[1-6]|li|ul|ol|tr|table)>", "\n", raw)
            raw = re.sub(r"(?s)<[^>]+>", " ", raw)
            raw = unescape(raw)
            raw = re.sub(r"[ \t\f\v]+", " ", raw)
            raw = re.sub(r"\n{3,}", "\n\n", raw)
            return "\n".join(line.rstrip() for line in raw.splitlines()).strip()
        return parser.text()

    def benchmark(self, html: str, iterations: int = 100) -> Dict[str, float]:
        if iterations <= 0:
            iterations = 1
        # Warm-up
        _ = self.get_text(html)
        start = time.perf_counter()
        last_text = ""
        for _i in range(iterations):
            last_text = self.get_text(html)
        duration = time.perf_counter() - start
        per_iter = duration / iterations
        return {
            "iterations": float(iterations),
            "seconds_total": float(duration),
            "seconds_per_iteration": float(per_iter),
            "chars": float(len(last_text)),
        }
