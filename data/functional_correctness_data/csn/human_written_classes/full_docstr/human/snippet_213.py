class BaseAuthenticationMiddleware:
    """Base class for all authentication middleware classes.

    Args:
        user_storage (BaseUserStorage): a storage object used to retrieve
            user object using their identifier lookup.
        name (str): custom name of the authentication middleware useful
            for handling custom user storage backends. Defaults to middleware
            class name.

    .. versionadded:: 0.4.0
    """
    challenge = None
    only_with_storage = False

    def __init__(self, user_storage=None, name=None):
        """Initialize authentication middleware."""
        self.user_storage = user_storage
        self.name = name if name else self.__class__.__name__
        if self.only_with_storage and (not isinstance(self.user_storage, BaseUserStorage)):
            raise ValueError('{} authentication middleware requires valid storage. Got {}.'.format(self.__class__.__name__, self.user_storage))

    def process_resource(self, req, resp, resource, uri_kwargs=None):
        """Process resource after routing to it.

        This is basic falcon middleware handler.

        Args:
            req (falcon.Request): request object
            resp (falcon.Response): response object
            resource (object): resource object matched by falcon router
            uri_kwargs (dict): additional keyword argument from uri template.
                For ``falcon<1.0.0`` this is always ``None``
        """
        if 'user' in req.context:
            return
        identifier = self.identify(req, resp, resource, uri_kwargs)
        user = self.try_storage(identifier, req, resp, resource, uri_kwargs)
        if user is not None:
            req.context['user'] = user
        elif self.challenge is not None:
            req.context.setdefault('challenges', list()).append(self.challenge)

    def identify(self, req, resp, resource, uri_kwargs):
        """Identify the user that made the request.

        Args:
            req (falcon.Request): request object
            resp (falcon.Response): response object
            resource (object): resource object matched by falcon router
            uri_kwargs (dict): additional keyword argument from uri template.
                For ``falcon<1.0.0`` this is always ``None``

        Returns:
            object: a user object (preferably a dictionary).
        """
        raise NotImplementedError

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        """Try to find user in configured user storage object.

        Args:
            identifier: User identifier.

        Returns:
            user object.
        """
        if identifier is None:
            user = None
        elif self.user_storage is not None:
            user = self.user_storage.get_user(self, identifier, req, resp, resource, uri_kwargs)
        elif self.user_storage is None and (not self.only_with_storage):
            user = {'identified_with': self, 'identifier': identifier}
        else:
            user = None
        return user