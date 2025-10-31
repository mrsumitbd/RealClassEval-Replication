
import re


class ShareClass:
    def __init__(self, service_number=None):
        self.service_number = service_number

    def canonical_uri(self, uri):
        return uri.strip().lower()

    def service_number(self):
        return self.service_number

    @staticmethod
    def magic():
        return "ShareClass"

    def extract(self, uri):
        canonical_uri = self.canonical_uri(uri)
        pattern = r'service/(\d+)'
        match = re.search(pattern, canonical_uri)
        if match:
            return match.group(1)
        else:
            return None


# Example usage:
if __name__ == "__main__":
    share_class = ShareClass()
    print(share_class.magic())  # Output: ShareClass
    print(share_class.canonical_uri("  Service/123  "))  # Output: service/123
    print(share_class.extract("https://example.com/service/123"))  # Output: 123
    print(share_class.extract("https://example.com/invalid-uri"))  # Output: None
