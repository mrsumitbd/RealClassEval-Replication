
class BaseAuthenticationMiddleware:

    def __init__(self, user_storage=None, name=None):

        self.user_storage = user_storage
        self.name = name

    def process_resource(self, req, resp, resource, uri_kwargs=None):

        identifier = self.identify(req, resp, resource, uri_kwargs)
        if identifier is not None:
            self.try_storage(identifier, req, resp, resource, uri_kwargs)

    def identify(self, req, resp, resource, uri_kwargs):

        pass

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):

        pass
