class SignatureComparator:

    def __init__(self, distance_threshold=5):
        self.distance_threshold = distance_threshold

    def from_entry(self, entry):
        return ContentSignature(code=entry.response.code, content_simhash=getattr(entry.result, 'content_simhash', None), content_hash=getattr(entry.result, 'content_hash', None), content_sample=getattr(entry.result, 'content_sample', None))

    def match(self, entry, signature, *, url):
        if signature is None:
            return False
        current = self.from_entry(entry)
        if current.code == signature.code:
            if signature.match_hash(current):
                return True
            if signature.match_simhash(current, self.distance_threshold):
                return True
            if signature.match_sample(current):
                return True
        return False

    def match_list(self, entry, signature_list, *, url):
        if signature_list is None:
            return False
        signature_list = signature_list if isinstance(signature_list, list) else [signature_list]
        for signature in signature_list:
            if self.match(entry, signature, url=url):
                return True
        return False