
class BaseAuthenticationMiddleware:

    def __init__(self, user_storage=None, name=None):
        self.user_storage = user_storage
        self.name = name

    def process_resource(self, req, resp, resource, uri_kwargs=None):
        if uri_kwargs is None:
            uri_kwargs = {}
        self.identify(req, resp, resource, uri_kwargs)

    def identify(self, req, resp, resource, uri_kwargs):
        identifier = self.extract_identifier(req)
        if identifier:
            self.try_storage(identifier, req, resp, resource, uri_kwargs)

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        if self.user_storage:
            user = self.user_storage.get(identifier)
            if user:
                req.context['user'] = user
            else:
                self.handle_unauthorized(req, resp)

    def extract_identifier(self, req):
        # This method should be overridden to extract the identifier from the request
        raise NotImplementedError(
            "This method should be overridden to extract the identifier from the request")

    def handle_unauthorized(self, req, resp):
        # This method should be overridden to handle unauthorized access
        raise NotImplementedError(
            "This method should be overridden to handle unauthorized access")
