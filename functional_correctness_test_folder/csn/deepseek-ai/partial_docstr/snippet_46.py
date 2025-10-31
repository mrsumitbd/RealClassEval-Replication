
class ShareClass:

    def canonical_uri(self, uri):
        pass

    def service_number(self):
        '''Return the service number.
        Returns:
            int: A number identifying the supported music service.
        '''
        pass

    @staticmethod
    def magic():
        pass

    def extract(self, uri):
        '''Extract the share type and encoded URI from a share link.
        Returns:
            share_type: The shared type, like "album" or "track".
            encoded_uri: An escaped URI with a service-specific format.
        '''
        pass
