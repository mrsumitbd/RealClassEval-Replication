
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
        if credentials:
            from flask import current_app
            current_app.auth = credentials

    def get_request_credentials(self):
        pass
