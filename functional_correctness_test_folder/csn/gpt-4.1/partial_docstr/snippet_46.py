
import re
from urllib.parse import urlparse, parse_qs, quote, unquote


class ShareClass:

    def canonical_uri(self, uri):
        # Normalize the URI: lowercase scheme/host, remove trailing slashes, decode/encode as needed
        parsed = urlparse(uri)
        scheme = parsed.scheme.lower()
        netloc = parsed.netloc.lower()
        path = parsed.path.rstrip('/')
        query = parsed.query
        fragment = parsed.fragment
        canonical = f"{scheme}://{netloc}{path}"
        if query:
            canonical += f"?{query}"
        if fragment:
            canonical += f"#{fragment}"
        return canonical

    def service_number(self):
        '''Return the service number.
        Returns:
            int: A number identifying the supported music service.
        '''
        # Example: Let's say 42 is the service number for this implementation
        return 42

    @staticmethod
    def magic():
        return "SHARE_MAGIC_2024"

    def extract(self, uri):
        '''Extract the share type and encoded URI from a share link.
        Returns:
            share_type: The shared type, like "album" or "track".
            encoded_uri: An escaped URI with a service-specific format.
        '''
        # Example: https://music.example.com/share/album/12345?uri=encoded_uri
        parsed = urlparse(uri)
        path_parts = parsed.path.strip('/').split('/')
        share_type = None
        encoded_uri = None

        # Try to extract share_type from path
        if len(path_parts) >= 2 and path_parts[0] == 'share':
            share_type = path_parts[1]
            # Try to get encoded_uri from query or from path
            qs = parse_qs(parsed.query)
            if 'uri' in qs:
                encoded_uri = qs['uri'][0]
            elif len(path_parts) >= 3:
                encoded_uri = quote(path_parts[2])
        else:
            # Fallback: try to match /sharetype/encoded_uri
            if len(path_parts) >= 2:
                share_type = path_parts[0]
                encoded_uri = quote(path_parts[1])

        return share_type, encoded_uri
