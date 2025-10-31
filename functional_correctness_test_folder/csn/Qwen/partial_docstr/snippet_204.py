
class AuthenticationBase:

    def authenticate_request(self):
        '''Store the request credentials in the
        :py:class:`flask.ctx.AppContext`.
        .. warning::
            No validation is performed by Flask-RESTy. It is up to the
            implementor to validate the request in
            :py:meth:`get_request_credentials`.
        '''
        credentials = self.get_request_credentials()
        from flask import g
        g.request_credentials = credentials

    def get_request_credentials(self):
        # This method should be overridden by subclasses to provide the actual logic
        # for extracting credentials from the request.
        raise NotImplementedError(
            "This method should be overridden to provide request credentials.")
