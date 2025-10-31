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
        uri_kwargs = uri_kwargs or {}
        user = self.identify(req, resp, resource, uri_kwargs)
        if user is not None:
            ctx = getattr(req, 'context', None)
            if ctx is None:
                try:
                    req.context = {}
                    ctx = req.context
                except Exception:
                    ctx = None
            if ctx is not None:
                try:
                    ctx['user'] = user
                except Exception:
                    try:
                        setattr(ctx, 'user', user)
                    except Exception:
                        pass

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
        raise NotImplementedError('Subclasses must implement identify()')

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        storage = self.user_storage
        if storage is None:
            return None

        # Try common callable retrieval methods
        method_names = (
            'get_user',
            'get',
            'get_by_id',
            'get_by_identifier',
            'retrieve',
            'fetch',
        )
        for name in method_names:
            getter = getattr(storage, name, None)
            if callable(getter):
                return getter(identifier)

        # Callable storage object
        if callable(storage):
            return storage(identifier)

        # Mapping-like storage
        try:
            return storage[identifier]  # type: ignore[index]
        except Exception:
            pass

        return None
