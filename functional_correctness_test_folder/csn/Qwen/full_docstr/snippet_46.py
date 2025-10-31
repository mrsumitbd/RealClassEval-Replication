
class ShareClass:
    '''Base class for supported services.'''

    def canonical_uri(self, uri):
        '''Recognize a share link and return its canonical representation.
        Args:
            uri (str): A URI like "https://tidal.com/browse/album/157273956".
        Returns:
            str: The canonical URI or None if not recognized.
        '''
        pass

    def service_number(self):
        '''Return the service number.
        Returns:
            int: A number identifying the supported music service.
        '''
        pass

    @staticmethod
    def magic():
        '''Return magic.
        Returns:
            dict: Magic prefix/key/class values for each share type.
        '''
        return {
            'tidal': {
                'album': 'https://tidal.com/browse/album/',
                'track': 'https://tidal.com/browse/track/'
            }
        }

    def extract(self, uri):
        '''Extract the share type and encoded URI from a share link.
        Returns:
            share_type: The shared type, like "album" or "track".
            encoded_uri: An escaped URI with a service-specific format.
        '''
        magic_values = self.magic().get('tidal', {})
        for share_type, prefix in magic_values.items():
            if uri.startswith(prefix):
                encoded_uri = uri[len(prefix):]
                return share_type, encoded_uri
        return None, None
