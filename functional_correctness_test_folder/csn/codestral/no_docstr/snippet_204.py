
class AuthenticationBase:

    def authenticate_request(self):
        """
        Authenticate the request.
        """
        pass

    def get_request_credentials(self):
        """
        Get the credentials from the request.
        """
        pass
