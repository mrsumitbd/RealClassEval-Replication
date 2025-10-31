class ShareClass:

    def canonical_uri(self, uri):
        share_type, encoded_uri = self.extract(uri)
        if not share_type or not encoded_uri:
            raise ValueError(
                "Unable to derive canonical URI from the given input")
        return f"share:{share_type}:{encoded_uri}"

    def service_number(self):
        '''Return the service number.
        Returns:
            int: A number identifying the supported music service.
        '''
        return 0

    @staticmethod
    def magic():
        return (
            r'^share:(album|track|playlist|artist):.+$',
            r'^https?://.+/(album|track|playlist|artist)/[^/?#]+',
            r'^https?://.+\?.*\buri=[^&#]+',
        )

    def extract(self, uri):
        '''Extract the share type and encoded URI from a share link.
        Returns:
            share_type: The shared type, like "album" or "track".
            encoded_uri: An escaped URI with a service-specific format.
        '''
        if not isinstance(uri, str) or not uri:
            raise ValueError("URI must be a non-empty string")

        # Case 1: share:<type>:<encoded>
        if uri.startswith("share:"):
            parts = uri.split(":", 2)
            if len(parts) >= 3:
                share_type = parts[1].lower()
                encoded_uri = parts[2]
                if share_type in {"album", "track", "playlist", "artist"} and encoded_uri:
                    return share_type, encoded_uri
            raise ValueError("Invalid share URI format")

        # Case 2: URL formats
        from urllib.parse import urlparse, parse_qs

        parsed = urlparse(uri)
        if not parsed.scheme or not parsed.netloc:
            raise ValueError("Invalid URI")

        # Try query param "uri" first (commonly percent-encoded full service URI)
        qs = parse_qs(parsed.query)
        if "uri" in qs and qs["uri"]:
            encoded_uri = qs["uri"][0]
            # Attempt to infer share_type from encoded service URI (e.g., spotify:track:...)
            # We do minimal parsing and keep encoded form as-is.
            maybe_decoded = encoded_uri
            # Determine share_type heuristically
            share_type = None
            # Try to detect pattern like scheme:type:...
            # We avoid unquoting to preserve "escaped URI" nature.
            colon_parts = maybe_decoded.split(":")
            if len(colon_parts) >= 2:
                inferred = colon_parts[1].lower()
                if inferred in {"album", "track", "playlist", "artist"}:
                    share_type = inferred
            # Fallback: derive from path segments
            if not share_type:
                segs = [s for s in parsed.path.split("/") if s]
                for seg in segs:
                    low = seg.lower()
                    if low in {"album", "track", "playlist", "artist"}:
                        share_type = low
                        break
            if not share_type:
                raise ValueError("Unable to determine share type from URI")
            return share_type, encoded_uri

        # Else derive from path: .../<type>/<id>(?...)?(#...)?
        segments = [s for s in parsed.path.split("/") if s]
        share_type = None
        encoded_uri = None
        for i, seg in enumerate(segments):
            low = seg.lower()
            if low in {"album", "track", "playlist", "artist"}:
                share_type = low
                # Next segment is typically the identifier
                if i + 1 < len(segments):
                    candidate = segments[i + 1]
                else:
                    candidate = ""
                # Strip query-like leftovers if any (shouldn't be present as we used path)
                # Keep as-is (already "encoded" enough for our purposes)
                encoded_uri = candidate
                break

        if not share_type or not encoded_uri:
            raise ValueError("Unsupported or unrecognized share URI format")

        return share_type, encoded_uri
