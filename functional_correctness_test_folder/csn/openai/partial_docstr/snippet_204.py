
from flask import g


class AuthenticationBase:
    """
    Base class for request authentication.

    Subclasses should implement :meth:`get_request_credentials` to extract
    credentials from the incoming request. The :meth:`authenticate_request`
    method will store those credentials in the Flask request context
    (``flask.g``) for later use.
    """

    def authenticate_request(self):
        """
        Store the request credentials in the Flask request context.

        No validation is performed by this base class. Subclasses must
        implement :meth:`get_request_credentials` to perform any
        necessary validation.
        """
        credentials = self.get_request_credentials()
        g.auth_credentials = credentials

    def get_request_credentials(self):
        """
        Extract credentials from the current request.

        Subclasses must override this method to provide the logic for
        retrieving and validating credentials from the request.
        """
        raise NotImplementedError(
            "Subclasses must implement get_request_credentials()"
        )
