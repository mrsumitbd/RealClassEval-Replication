from abc import ABC, abstractmethod


class AuthenticationBase(ABC):
    @abstractmethod
    def authenticate_request(self):
        raise NotImplementedError(
            "Subclasses must implement authenticate_request()")

    @abstractmethod
    def get_request_credentials(self):
        raise NotImplementedError(
            "Subclasses must implement get_request_credentials()")
