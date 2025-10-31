
import re
from urllib.parse import unquote


class ShareClass:

    def canonical_uri(self, uri):
        share_type, encoded_uri = self.extract(uri)
        return f"{share_type}:{unquote(encoded_uri)}"

    def service_number(self):
        '''Return the service number.
        Returns:
            int: A number identifying the supported music service.
        '''
        return 1  # Replace with actual service number

    @staticmethod
    def magic():
        return "magic_string"  # Replace with actual magic string

    def extract(self, uri):
        '''Extract the share type and encoded URI from a share link.
        Returns:
            share_type: The shared type, like "album" or "track".
            encoded_uri: An escaped URI with a service-specific format.
        '''
        # Assuming the URI is in the format https://example.com/{share_type}/{encoded_uri}
        pattern = r"^https?://example\.com/(album|track)/([^/]+)"
        match = re.match(pattern, uri)
        if match:
            share_type = match.group(1)
            encoded_uri = match.group(2)
            return share_type, encoded_uri
        else:
            raise ValueError("Invalid URI format")
