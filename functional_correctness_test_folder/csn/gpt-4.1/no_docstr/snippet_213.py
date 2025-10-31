
class BaseAuthenticationMiddleware:

    def __init__(self, user_storage=None, name=None):
        self.user_storage = user_storage
        self.name = name

    def process_resource(self, req, resp, resource, uri_kwargs=None):
        if uri_kwargs is None:
            uri_kwargs = {}
        user = self.identify(req, resp, resource, uri_kwargs)
        req.context = getattr(req, 'context', {})
        req.context['user'] = user

    def identify(self, req, resp, resource, uri_kwargs):
        identifier = None
        if hasattr(req, 'headers') and 'Authorization' in req.headers:
            identifier = req.headers['Authorization']
        elif hasattr(req, 'cookies') and 'auth_token' in req.cookies:
            identifier = req.cookies['auth_token']
        if identifier:
            user = self.try_storage(
                identifier, req, resp, resource, uri_kwargs)
            return user
        return None

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        if self.user_storage is not None and hasattr(self.user_storage, 'get'):
            return self.user_storage.get(identifier)
        return None
