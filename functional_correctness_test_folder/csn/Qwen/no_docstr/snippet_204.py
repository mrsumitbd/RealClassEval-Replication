
class AuthenticationBase:

    def authenticate_request(self):
        raise NotImplementedError(
            "This method should be overridden by subclasses to authenticate a request.")

    def get_request_credentials(self):
        raise NotImplementedError(
            "This method should be overridden by subclasses to retrieve request credentials.")
