
from flask import g


class AuthenticationBase:
    def authenticate_request(self):
        """Store the request credentials in the
        :py:class:`flask.ctx.AppContext`.
        .. warning::
            No validation is performed by Flask-RESTy. It is up to the
            implementor to validate the request in
            :py:meth:`get_request_credentials`.
        """
        g.request_credentials = self.get_request_credentials()

    def get_request_credentials(self):
        raise NotImplementedError(
            "Subclasses must implement get_request_credentials")
