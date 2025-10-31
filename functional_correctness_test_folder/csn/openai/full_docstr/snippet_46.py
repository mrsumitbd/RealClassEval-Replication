
import re
from urllib.parse import urlparse, unquote


class ShareClass:
    '''Base class for supported services.'''

    def canonical_uri(self, uri):
        '''Recognize a share link and return its canonical representation.
        Args:
            uri (str): A URI like "https://tidal.com/browse/album/157273956".
        Returns:
            str: The canonical URI or None if not recognized.
        '''
        if not isinstance(uri, str):
            return None
        parsed = urlparse(uri)
        if parsed.scheme not in ('http', 'https'):
            return None
        # Basic normalization: lower-case scheme and netloc, strip trailing slash
        netloc = parsed.netloc.lower()
        path = parsed.path.rstrip('/')
        canonical = f'{parsed.scheme}://{netloc}{path}'
        return canonical

    def service_number(self):
        '''Return the service number.
        Returns:
            int: A number identifying the supported music service.
        '''
        return 0

    @staticmethod
    def magic():
        '''Return magic.
        Returns:
            dict: Magic prefix/key/class values for each share type.
        '''
        return {}

    def extract(self, uri):
        '''Extract the share type and encoded URI from a share link.
        Returns:
            share_type: The shared type, like "album" or "track".
            encoded_uri: An escaped URI with a service‑specific format.
        '''
        if not isinstance(uri, str):
            return None, None
        parsed = urlparse(uri)
        if not parsed.path:
            return None, None
        # Split path into segments, ignore leading slash
        segments = [seg for seg in parsed.path.split('/') if seg]
        if not segments:
            return None, None
        share_type = segments[0]
        # Encode the URI (percent‑encode any non‑ASCII characters)
        encoded_uri = unquote(uri)
        return share_type, encoded_uri
