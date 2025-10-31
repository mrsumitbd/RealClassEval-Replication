
class ShareClass:

    def canonical_uri(self, uri):
        return uri.strip().lower()

    def service_number(self):
        return 42

    @staticmethod
    def magic():
        return "Abracadabra"

    def extract(self, uri):
        parts = uri.split('/')
        return parts[-1] if parts else ""
