
class BaseAuthenticationMiddleware:

    def __init__(self, user_storage=None, name=None):
        self.user_storage = user_storage
        self.name = name

    def process_resource(self, req, resp, resource, uri_kwargs=None):
        if uri_kwargs is None:
            uri_kwargs = {}
        self.identify(req, resp, resource, uri_kwargs)

    def identify(self, req, resp, resource, uri_kwargs):
        raise NotImplementedError("Subclasses must implement this method.")

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        if self.user_storage is not None:
            return self.user_storage.get(identifier)
        return None
