
class AuthenticationBase:

    def authenticate_request(self):
        """
        Authenticate the request.
        Should be implemented by subclasses.
        """
        raise NotImplementedError(
            "Subclasses must implement authenticate_request()")

    def get_request_credentials(self):
        """
        Get credentials from the request.
        Should be implemented by subclasses.
        """
        raise NotImplementedError(
            "Subclasses must implement get_request_credentials()")
