
class BaseAuthenticationMiddleware:

    def __init__(self, user_storage=None, name=None):
        """
        Initialize the BaseAuthenticationMiddleware.

        :param user_storage: The storage for user data.
        :param name: The name of the authentication middleware.
        """
        self.user_storage = user_storage
        self.name = name

    def process_resource(self, req, resp, resource, uri_kwargs=None):
        """
        Process the incoming request and authenticate if necessary.

        :param req: The incoming request.
        :param resp: The outgoing response.
        :param resource: The resource being requested.
        :param uri_kwargs: Keyword arguments from the URI template.
        """
        self.identify(req, resp, resource, uri_kwargs)

    def identify(self, req, resp, resource, uri_kwargs):
        """
        Identify the user making the request.

        :param req: The incoming request.
        :param resp: The outgoing response.
        :param resource: The resource being requested.
        :param uri_kwargs: Keyword arguments from the URI template.
        :raises NotImplementedError: If not implemented by a subclass.
        """
        raise NotImplementedError(
            "Subclasses must implement the 'identify' method.")

    def try_storage(self, identifier, req, resp, resource, uri_kwargs):
        """
        Attempt to retrieve user data from storage using the given identifier.

        :param identifier: The identifier to use when retrieving user data.
        :param req: The incoming request.
        :param resp: The outgoing response.
        :param resource: The resource being requested.
        :param uri_kwargs: Keyword arguments from the URI template.
        :return: The user data if found, otherwise None.
        """
        if self.user_storage is not None:
            return self.user_storage.get(identifier)
        return None
