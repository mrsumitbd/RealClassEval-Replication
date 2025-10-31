
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
        self.name = name or self.__class__.__name__

    def process_resource(self, req, resp, resource, uri_kwargs=None):
        """
        Falcon middleware hook that runs before the resource method.
        It attempts to identify the user making the request and attaches
        the user object to the request context.
        """
        if uri_kwargs is None:
            uri_kwargs = {}
        user = self.identify(req, resp, resource, uri_kwargs)
        if user is not None:
            # Attach user to request context for downstream use
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
        raise NotImplementedError(
            f"{self.__class__.__name__}.identify() must be overridden"
        )

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        """
        Attempt to retrieve a user from the configured storage backend
        using the provided identifier.  If the storage backend is not
        configured or the identifier cannot be resolved, ``None`` is
        returned.
        """
        if self.user_storage is None:
            return None
        # The storage backend is expected to provide a ``get_user`` method.
        get_user = getattr(self.user_storage, "get_user", None)
        if get_user is None:
            return None
        try:
            return get_user(identifier)
        except Exception:
            # Any error (e.g., user not found) results in None
            return None
