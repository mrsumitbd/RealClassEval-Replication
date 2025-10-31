class AbstractHtmlConverter:
    def get_text(self, html):
        '''
        Returns:
            a text representation of the given HTML snippet.
        '''
        from html.parser import HTMLParser
        from html import unescape
        import re

        if html is None:
            return ""

        class _TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__(convert_charrefs=False)
                self._buf = []
                self._suppress = 0  # depth counter for script/style
                self._pre = 0       # depth counter for preformatted blocks

            def _newline(self):
                if not self._buf:
                    self._buf.append("\n")
                    return
                if self._buf[-1].endswith("\n"):
                    return
                self._buf.append("\n")

            def handle_starttag(self, tag, attrs):
                t = tag.lower()
                if t in ("script", "style"):
                    self._suppress += 1
                    return

                if t in ("br",):
                    self._newline()
                elif t in ("p", "div", "section", "article", "header", "footer", "aside",
                           "ul", "ol", "li", "table", "tr", "td", "th", "thead", "tbody",
                           "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "hr"):
                    self._newline()
                elif t in ("pre",):
                    self._pre += 1
                    self._newline()

                if t == "li":
                    # bullet prefix
                    self._buf.append("- ")

            def handle_endtag(self, tag):
                t = tag.lower()
                if t in ("script", "style"):
                    if self._suppress > 0:
                        self._suppress -= 1
                    return

                if t in ("p", "div", "section", "article", "header", "footer", "aside",
                         "ul", "ol", "li", "table", "tr", "td", "th", "thead", "tbody",
                         "h1", "h2", "h3", "h4", "h5", "h6", "blockquote", "pre"):
                    self._newline()

                if t == "pre" and self._pre > 0:
                    self._pre -= 1

            def handle_data(self, data):
                if self._suppress:
                    return
                if not data:
                    return
                if self._pre:
                    self._buf.append(data)
                else:
                    self._buf.append(data)

            def handle_entityref(self, name):
                if self._suppress:
                    return
                self._buf.append(unescape(f"&{name};"))

            def handle_charref(self, name):
                if self._suppress:
                    return
                self._buf.append(unescape(f"&#{name};"))

            def get_text(self):
                text = "".join(self._buf)
                text = unescape(text)

                # Normalize whitespace outside of pre blocks effect, but since we can't
                # reconstruct exact ranges post-parse, we approximate:
                # - collapse spaces/tabs
                # - normalize line endings
                text = text.replace("\r\n", "\n").replace("\r", "\n")

                # Collapse spaces around newlines
                text = re.sub(r"[ \t]+\n", "\n", text)
                text = re.sub(r"\n[ \t]+", "\n", text)

                # Collapse multiple spaces
                text = re.sub(r"[ \t]{2,}", " ", text)

                # Collapse excessive blank lines to at most two newlines
                text = re.sub(r"\n{3,}", "\n\n", text)

                # Trim leading/trailing whitespace
                return text.strip()

        parser = _TextExtractor()
        try:
            parser.feed(str(html))
            parser.close()
        except Exception:
            # Fallback: very naive strip tags
            import re as _re
            raw = _re.sub(r"(?is)<(script|style).*?</\1>", "", str(html))
            raw = _re.sub(r"(?is)<br\s*/?>", "\n", raw)
            raw = _re.sub(
                r"(?is)</?(p|div|li|tr|h[1-6]|blockquote|pre|section|article|header|footer|aside)[^>]*>", "\n", raw)
            raw = _re.sub(r"(?is)<.*?>", "", raw)
            text = unescape(raw)
            text = _re.sub(r"[ \t]+", " ", text)
            text = _re.sub(r"\n{3,}", "\n\n", text)
            return text.strip()

        return parser.get_text()

    def benchmark(self, html):
        import time

        # Warm-up
        self.get_text(html)

        min_runtime = 0.2
        iterations = 1
        total = 0.0

        while total < min_runtime and iterations < 100000:
            start = time.perf_counter()
            for _ in range(iterations):
                self.get_text(html)
            end = time.perf_counter()
            total = end - start
            if total < min_runtime:
                iterations *= 2

        per_call = total / iterations if iterations else float("inf")
        ips = (1.0 / per_call) if per_call > 0 else float("inf")

        return {
            "iterations": iterations,
            "total_seconds": total,
            "seconds_per_call": per_call,
            "iterations_per_second": ips,
        }
