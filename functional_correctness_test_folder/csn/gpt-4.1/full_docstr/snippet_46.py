
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
        parsed = urlparse(uri)
        if not parsed.scheme.startswith('http'):
            return None
        # Example: https://tidal.com/browse/album/157273956
        m = re.match(
            r'^/(browse/)?(?P<type>album|track|playlist|artist)/(?P<id>[A-Za-z0-9]+)', parsed.path)
        if m:
            share_type = m.group('type')
            share_id = m.group('id')
            return f"{parsed.scheme}://{parsed.netloc}/browse/{share_type}/{share_id}"
        return None

    def service_number(self):
        '''Return the service number.
        Returns:
            int: A number identifying the supported music service.
        '''
        # Example: 1 for Tidal, 2 for Spotify, etc. Here, just return 0 as base.
        return 0

    @staticmethod
    def magic():
        '''Return magic.
        Returns:
            dict: Magic prefix/key/class values for each share type.
        '''
        return {
            'album': {'prefix': 'al', 'key': 'album', 'class': 'AlbumShare'},
            'track': {'prefix': 'tr', 'key': 'track', 'class': 'TrackShare'},
            'playlist': {'prefix': 'pl', 'key': 'playlist', 'class': 'PlaylistShare'},
            'artist': {'prefix': 'ar', 'key': 'artist', 'class': 'ArtistShare'},
        }

    def extract(self, uri):
        '''Extract the share type and encoded URI from a share link.
        Returns:
            share_type: The shared type, like "album" or "track".
            encoded_uri: An escaped URI with a service-specific format.
        '''
        parsed = urlparse(uri)
        m = re.match(
            r'^/(browse/)?(?P<type>album|track|playlist|artist)/(?P<id>[A-Za-z0-9]+)', parsed.path)
        if m:
            share_type = m.group('type')
            share_id = m.group('id')
            encoded_uri = f"{share_type}:{share_id}"
            return share_type, encoded_uri
        return None, None
