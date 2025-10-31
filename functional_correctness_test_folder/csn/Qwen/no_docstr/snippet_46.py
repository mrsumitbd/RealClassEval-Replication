
class ShareClass:

    def canonical_uri(self, uri):
        return uri.strip().lower()

    def service_number(self):
        return hash(self) % 1000

    @staticmethod
    def magic():
        return 42

    def extract(self, uri):
        return uri.split('/')[-1]
