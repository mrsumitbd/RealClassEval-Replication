
import falcon


class BaseAuthenticationMiddleware:
    """
    A simple authentication middleware that extracts a bearer token from the
    `Authorization` header, looks up a user in the provided storage, and
    attaches the user object to the request context.
    """

    def __init__(self, user_storage=None, name=None):
        """
        Parameters
        ----------
        user_storage : Mapping or callable, optional
            Storage that can return a user object given an identifier.
            If a mapping, the identifier is used as a key.
            If a callable, it is called with the identifier.
            If it has a `get_user` method, that method is used.
        name : str, optional
            Name used as the key in `req.context` to store the user.
        """
        self.user_storage = user_storage
        self.name = name or "user"

    def process_resource(self, req, resp, resource, uri_kwargs=None):
        """
        Called by Falcon before the resource method is invoked.
        Identifies the user and stores it in the request context.
        """
        identifier = self.identify(req, resp, resource, uri_kwargs)
        if identifier:
            user = self.try_storage(
                identifier, req, resp, resource, uri_kwargs)
            req.context[self.name] = user
        else:
            req.context[self.name] = None

    def identify(self, req, resp, resource, uri_kwargs):
        """
        Extracts an identifier (token) from the `Authorization` header.
        Supports the `Bearer <token>` scheme.
        """
        auth_header = req.get_header("Authorization")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2:
            return None

        scheme, token = parts
        if scheme.lower() != "bearer":
            return None

        return token

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        """
        Looks up the user in the configured storage.
        Raises `falcon.HTTPUnauthorized` if the user cannot be found.
        """
        if self.user_storage is None:
            raise falcon.HTTPUnauthorized(
                "Authentication required",
                "No user storage configured",
            )

        # Mapping lookup
        if isinstance(self.user_storage, dict):
            user = self.user_storage.get(identifier)
        # Object with get_user method
        elif hasattr(self.user_storage, "get_user"):
            user = self.user_storage.get_user(identifier)
        # Callable
        elif callable(self.user_storage):
            user = self.user_storage(identifier)
        else:
            user = None

        if user is None:
            raise falcon.HTTPUnauthorized(
                "Authentication required",
                "Invalid credentials",
            )

        return user
