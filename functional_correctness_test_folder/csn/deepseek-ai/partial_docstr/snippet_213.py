
class BaseAuthenticationMiddleware:
    '''Base class for all authentication middleware classes.
    Args:
        user_storage (BaseUserStorage): a storage object used to retrieve
            user object using their identifier lookup.
        name (str): custom name of the authentication middleware useful
            for handling custom user storage backends. Defaults to middleware
            class name.
    .. versionadded:: 0.4.0
    '''

    def __init__(self, user_storage=None, name=None):
        self.user_storage = user_storage
        self.name = name if name is not None else self.__class__.__name__

    def process_resource(self, req, resp, resource, uri_kwargs=None):
        user = self.identify(req, resp, resource, uri_kwargs)
        if user is not None:
            req.context['user'] = user

    def identify(self, req, resp, resource, uri_kwargs):
        '''Identify the user that made the request.
        Args:
            req (falcon.Request): request object
            resp (falcon.Response): response object
            resource (object): resource object matched by falcon router
            uri_kwargs (dict): additional keyword argument from uri template.
                For ``falcon<1.0.0`` this is always ``None``
        Returns:
            object: a user object (preferably a dictionary).
        '''
        raise NotImplementedError

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        if self.user_storage is not None:
            return self.user_storage.get_user(identifier)
        return None
