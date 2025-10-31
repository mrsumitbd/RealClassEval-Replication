
import urllib.parse


class ShareClass:
    def canonical_uri(self, uri):
        """
        Return a canonical form of the given URI.
        For the base implementation this simply normalises the scheme and host
        to lower case and removes any trailing slash.
        """
        if not uri:
            return uri
        parsed = urllib.parse.urlparse(uri)
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()
        path = parsed.path.rstrip("/")
        # Rebuild the URI without fragment
        canonical = urllib.parse.urlunparse(
            (scheme, netloc, path, parsed.params, parsed.query, "")
        )
        return canonical

    def service_number(self):
        """
        Return the service number.
        Returns:
            int: A number identifying the supported music service.
        """
        # Base class has no specific service; return 0
        return 0

    @staticmethod
    def magic():
        """
        Return a magic string used by subclasses for identification.
        """
        return "magic"

    def extract(self, uri):
        """
        Extract the share type and encoded URI from a share link.
        Returns:
            share_type: The shared type, like "album" or "track".
            encoded_uri: An escaped URI with a service‑specific format.
        """
        if not uri:
            return None, None
        parsed = urllib.parse.urlparse(uri)
        # Split the path into segments, ignoring empty ones
        segments = [seg for seg in parsed.path.split("/") if seg]
        if not segments:
            return None, None
        share_type = segments[0]
        # Reconstruct the encoded part: everything after the share_type
        encoded_path = "/".join(segments[1:])
        if parsed.query:
            encoded_path = f"{encoded_path}?{parsed.query}"
        return share_type, encoded_path
