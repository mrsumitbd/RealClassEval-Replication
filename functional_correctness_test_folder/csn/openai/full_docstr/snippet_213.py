
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
        if user_storage is None:
            raise ValueError("user_storage must be provided")
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
        # Store the user in the request context for downstream handlers
        if not hasattr(req, 'context'):
            req.context = {}
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
        # Attempt to extract an identifier from common sources
        identifier = None

        # 1. Header
        if hasattr(req, 'get_header'):
            identifier = req.get_header('X-User-Id')
        # 2. Query parameter
        if not identifier and hasattr(req, 'params'):
            identifier = req.params.get('user_id')
        # 3. URI kwargs
        if not identifier and uri_kwargs:
            identifier = uri_kwargs.get('user_id')

        if not identifier:
            return None

        return self.try_storage(identifier, req, resp, resource, uri_kwargs)

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        '''Try to find user in configured user storage object.
        Args:
            identifier: User identifier.
        Returns:
            user object.
        '''
        try:
            # The storage is expected to provide a get_user method
            return self.user_storage.get_user(identifier)
        except Exception:
            # If storage lookup fails, return None
            return None
