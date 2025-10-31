
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
        share_type, encoded_uri = self.extract(uri)
        if share_type and encoded_uri:
            return f"{self.service_number()}:{share_type}:{encoded_uri}"
        return None

    def service_number(self):
        '''Return the service number.
        Returns:
            int: A number identifying the supported music service.
        '''
        raise NotImplementedError("Subclass must implement service_number")

    @staticmethod
    def magic():
        '''Return magic.
        Returns:
            dict: Magic prefix/key/class values for each share type.
        '''
        raise NotImplementedError("Subclass must implement magic")

    def extract(self, uri):
        '''Extract the share type and encoded URI from a share link.
        Returns:
            share_type: The shared type, like "album" or "track".
            encoded_uri: An escaped URI with a service-specific format.
        '''
        parsed_uri = urlparse(uri)
        path = unquote(parsed_uri.path)
        magic = self.magic()
        for share_type, magic_values in magic.items():
            pattern = re.compile(magic_values['pattern'])
            match = pattern.search(path)
            if match:
                encoded_uri = match.group(1)
                return share_type, encoded_uri
        return None, None
