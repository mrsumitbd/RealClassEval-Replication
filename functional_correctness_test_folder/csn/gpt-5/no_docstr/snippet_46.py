class ShareClass:
    def canonical_uri(self, uri):
        if uri is None:
            return None
        if not isinstance(uri, str):
            raise TypeError("uri must be a string or None")
        uri = uri.strip()
        if not uri:
            return None

        from urllib.parse import urlparse, urlunparse, quote, unquote

        # Prepend scheme if missing
        if "://" not in uri and uri.startswith("www."):
            uri = "http://" + uri
        elif "://" not in uri and not uri.startswith(("http://", "https://")):
            uri = "http://" + uri

        parsed = urlparse(uri)

        scheme = (parsed.scheme or "http").lower()
        netloc = parsed.netloc.lower()

        # Remove default ports
        if netloc.endswith(":80") and scheme == "http":
            netloc = netloc[:-3]
        elif netloc.endswith(":443") and scheme == "https":
            netloc = netloc[:-4]

        # Normalize path: remove duplicate slashes, percent-encode unsafe chars
        path = parsed.path or "/"
        while "//" in path:
            path = path.replace("//", "/")

        # Remove trailing slash unless root
        if path != "/" and path.endswith("/"):
            path = path[:-1]

        # Normalize percent-encoding (decode then re-encode)
        try:
            path = quote(unquote(path), safe="/:@&+$,;=-._~()")
        except Exception:
            pass

        # Sort query parameters
        query = parsed.query
        if query:
            from urllib.parse import parse_qsl, urlencode
            qsl = parse_qsl(query, keep_blank_values=True)
            qsl.sort()
            query = urlencode(qsl, doseq=True)

        fragment = ""  # drop fragment for canonical form

        canonical = urlunparse((scheme, netloc, path, "", query, fragment))
        return canonical

    def service_number(self):
        # Stable deterministic number based on class name
        import hashlib
        h = hashlib.md5(self.__class__.__name__.encode("utf-8")).hexdigest()
        return int(h[:8], 16)

    @staticmethod
    def magic():
        return "magic"

    def extract(self, uri):
        """
        Extract a likely share identifier from the URI.
        Preference order:
        - Query params: id, share_id, share, s
        - Last non-empty path segment
        Returns None if nothing reasonable is found.
        """
        from urllib.parse import urlparse, parse_qs

        canon = self.canonical_uri(uri)
        if not canon:
            return None

        parsed = urlparse(canon)
        qs = parse_qs(parsed.query)

        for key in ("id", "share_id", "share", "s"):
            if key in qs and qs[key]:
                val = qs[key][0].strip()
                if val:
                    return val

        # Last non-empty path segment
        segments = [seg for seg in (parsed.path or "").split("/") if seg]
        if segments:
            return segments[-1]

        return None
