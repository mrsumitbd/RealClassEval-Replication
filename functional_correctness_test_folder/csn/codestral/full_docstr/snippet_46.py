
class ShareClass:
    '''Base class for supported services.'''

    def canonical_uri(self, uri):
        '''Recognize a share link and return its canonical representation.
        Args:
            uri (str): A URI like "https://tidal.com/browse/album/157273956".
        Returns:
            str: The canonical URI or None if not recognized.
        '''
        # Implementation for recognizing and returning the canonical URI
        pass

    def service_number(self):
        '''Return the service number.
        Returns:
            int: A number identifying the supported music service.
        '''
        # Implementation for returning the service number
        pass

    @staticmethod
    def magic():
        '''Return magic.
        Returns:
            dict: Magic prefix/key/class values for each share type.
        '''
        # Implementation for returning magic prefix/key/class values
        pass

    def extract(self, uri):
        '''Extract the share type and encoded URI from a share link.
        Returns:
            share_type: The shared type, like "album" or "track".
            encoded_uri: An escaped URI with a service-specific format.
        '''
        # Implementation for extracting the share type and encoded URI
        pass
