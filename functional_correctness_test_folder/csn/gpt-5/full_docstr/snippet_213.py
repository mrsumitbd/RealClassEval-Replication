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
        # Attach identified user onto the request in a best-effort manner
        try:
            if hasattr(req, 'context') and req.context is not None:
                ctx = req.context
                # dict-like context
                if isinstance(ctx, dict):
                    ctx['user'] = user
                else:
                    # object-like context
                    try:
                        setattr(ctx, 'user', user)
                    except Exception:
                        pass
        except Exception:
            pass
        # Also attach directly on request for convenience
        try:
            setattr(req, 'user', user)
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
        return None

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        '''Try to find user in configured user storage object.
        Args:
            identifier: User identifier.
        Returns:
            user object.
        '''
        if identifier is None or self.user_storage is None:
            return None

        storage = self.user_storage

        # If storage is callable (factory/lookup), try calling with identifier
        try:
            if callable(storage):
                user = storage(identifier)
                if user is not None:
                    return user
        except Exception:
            pass

        # Try common lookup methods
        methods = (
            'get',
            'get_user',
            'get_by_id',
            'find',
            'lookup',
            'retrieve',
            'fetch',
        )
        for m in methods:
            try:
                meth = getattr(storage, m, None)
                if callable(meth):
                    user = meth(identifier)
                    if user is not None:
                        return user
            except Exception:
                continue

        # Mapping-style access
        try:
            if isinstance(storage, dict):
                return storage.get(identifier)
        except Exception:
            pass

        try:
            # __getitem__ style
            return storage[identifier]  # type: ignore[index]
        except Exception:
            pass

        return None
