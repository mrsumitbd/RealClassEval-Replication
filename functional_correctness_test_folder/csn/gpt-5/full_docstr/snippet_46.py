import re
from urllib.parse import urlsplit, urlunsplit, quote, unquote


class ShareClass:
    '''Base class for supported services.'''

    def canonical_uri(self, uri):
        '''Recognize a share link and return its canonical representation.
        Args:
            uri (str): A URI like "https://tidal.com/browse/album/157273956".
        Returns:
            str: The canonical URI or None if not recognized.
        '''
        if not uri or not isinstance(uri, str):
            return None

        parts = urlsplit(uri.strip())
        if not parts.scheme or not parts.netloc:
            return None

        scheme = parts.scheme.lower()
        netloc = parts.netloc.lower()

        # Strip default ports
        host, sep, port = netloc.partition(':')
        if (scheme == 'http' and port == '80') or (scheme == 'https' and port == '443'):
            netloc = host

        # Normalize path: remove multiple slashes, strip trailing slash, keep leading slash
        path = unquote(parts.path or '')
        path = re.sub(r'/+', '/', path)
        if path != '/' and path.endswith('/'):
            path = path[:-1]
        # Ensure it starts with a single slash if non-empty
        if path and not path.startswith('/'):
            path = '/' + path
        path = quote(path, safe='/-._~')

        # Remove query and fragment for canonical
        canonical = urlunsplit((scheme, netloc, path, '', ''))
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
            encoded_uri: An escaped URI with a service-specific format.
        '''
        canon = self.canonical_uri(uri)
        if not canon:
            return None, None

        path = urlsplit(canon).path or ''
        segments = [seg for seg in path.split('/') if seg]

        share_type = None
        if segments:
            # Heuristic: pick the last textual segment that isn't purely numeric as the type,
            # otherwise take the preceding one if available.
            if len(segments) >= 2:
                if not segments[-1].isalpha() and segments[-2].isalpha():
                    share_type = segments[-2]
                elif segments[-1].isalpha():
                    share_type = segments[-1]
                else:
                    # fallback to second last if exists
                    share_type = segments[-2]
            else:
                share_type = segments[-1]

        encoded_uri = canon
        return share_type, encoded_uri
