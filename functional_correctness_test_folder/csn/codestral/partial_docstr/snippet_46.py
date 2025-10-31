
class ShareClass:

    def canonical_uri(self, uri):
        return uri.lower().strip()

    def service_number(self):
        return 1

    @staticmethod
    def magic():
        return "magic"

    def extract(self, uri):
        parts = uri.split(':')
        if len(parts) >= 3:
            share_type = parts[1]
            encoded_uri = ':'.join(parts[2:])
            return share_type, encoded_uri
        return None, None
