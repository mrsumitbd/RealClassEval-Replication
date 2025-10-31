from flask import g


class AuthenticationBase:
    CONTEXT_KEY = "auth_credentials"

    def authenticate_request(self):
        '''Store the request credentials in the
        :py:class:`flask.ctx.AppContext`.
        .. warning::
            No validation is performed by Flask-RESTy. It is up to the
            implementor to validate the request in
            :py:meth:`get_request_credentials`.
        '''
        creds = self.get_request_credentials()
        setattr(g, self.CONTEXT_KEY, creds)
        return creds

    def get_request_credentials(self):
        raise NotImplementedError(
            "Subclasses must implement get_request_credentials()")
