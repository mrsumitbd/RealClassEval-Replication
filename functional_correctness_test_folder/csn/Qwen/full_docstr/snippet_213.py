
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
        '''Initialize authentication middleware.'''
        self.user_storage = user_storage
        self.name = name or self.__class__.__name__

    def process_resource(self, req, resp, resource, uri_kwargs=None):
        '''Process resource after routing to it.
        This is basic falcon middleware handler.
        Args:
            req (falcon.Request): request object
            resp (falcon.Response): response object
            resource (object): resource object matched by falcon router
            uri_kwargs (dict): additional keyword argument from uri template.
                For ``falcon<1.0.0`` this is always ``None``
        '''
        user = self.identify(req, resp, resource, uri_kwargs)
        if user:
            req.context['user'] = user
        else:
            resp.status = falcon.HTTP_401
            resp.body = 'Unauthorized'

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
        identifier = self.extract_identifier(req)
        if identifier:
            return self.try_storage(identifier, req, resp, resource, uri_kwargs)
        return None

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        '''Try to find user in configured user storage object.
        Args:
            identifier: User identifier.
        Returns:
            user object.
        '''
        if self.user_storage:
            return self.user_storage.get_user(identifier)
        return None

    def extract_identifier(self, req):
        '''Extract user identifier from the request.
        Args:
            req (falcon.Request): request object
        Returns:
            identifier: User identifier.
        '''
        # This method should be overridden by subclasses to extract the identifier
        # from the request, e.g., from headers, cookies, etc.
        return None
