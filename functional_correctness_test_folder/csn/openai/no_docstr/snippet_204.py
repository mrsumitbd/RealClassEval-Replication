class AuthenticationBase:
    def authenticate_request(self):
        raise NotImplementedError(
            "Subclasses must implement authenticate_request")

    def get_request_credentials(self):
        raise NotImplementedError(
            "Subclasses must implement get_request_credentials")
