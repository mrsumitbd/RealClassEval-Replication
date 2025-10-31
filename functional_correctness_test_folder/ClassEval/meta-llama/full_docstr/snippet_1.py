
import logging
from datetime import datetime


class AccessGatewayFilter:
    """
    This class is a filter used for accessing gateway filtering, primarily for authentication and access log recording.
    """

    def __init__(self):
        self.allowed_prefixes = ['/api', '/login']
        self.logger = logging.getLogger(__name__)

    def filter(self, request):
        """
        Filter the incoming request based on certain rules and conditions.
        :param request: dict, the incoming request details
        :return: bool, True if the request is allowed, False otherwise
        >>> filter = AccessGatewayFilter()
        >>> filter.filter({'path': '/login', 'method': 'POST'})
        True

        """
        if 'path' not in request or 'method' not in request:
            return False

        request_uri = request['path']
        if self.is_start_with(request_uri):
            if request['method'] == 'POST' and request_uri == '/login':
                return True
            user = self.get_jwt_user(request)
            if user is not None:
                self.set_current_user_info_and_log(user)
                return True
        return False

    def is_start_with(self, request_uri):
        """
        Check if the request URI starts with certain prefixes.
        Currently, the prefixes being checked are "/api" and "/login".
        :param request_uri: str, the URI of the request
        :return: bool, True if the URI starts with certain prefixes, False otherwise
        >>> filter = AccessGatewayFilter()
        >>> filter.is_start_with('/api/data')
        True

        """
        for prefix in self.allowed_prefixes:
            if request_uri.startswith(prefix):
                return True
        return False

    def get_jwt_user(self, request):
        """
        Get the user information from the JWT token in the request.
        :param request: dict, the incoming request details
        :return: dict or None, the user information if the token is valid, None otherwise
        >>> filter = AccessGatewayFilter()
        >>> filter.get_jwt_user({'headers': {'Authorization': 'user1'+str(datetime.date.today())}})
        'user1...'

        """
        if 'headers' in request and 'Authorization' in request['headers']:
            auth_header = request['headers']['Authorization']
            # Here we assume that the 'Authorization' header contains a dictionary with 'user' and 'jwt' keys.
            # In a real-world scenario, you would need to parse the JWT token and verify its validity.
            if isinstance(auth_header, dict) and 'user' in auth_header:
                return auth_header['user']
            # For simplicity, let's assume the 'Authorization' header is a string that contains the user information.
            elif isinstance(auth_header, str):
                # In a real application, you should validate the JWT token here.
                # For demonstration purposes, we will just return a dummy user.
                return {'name': 'user1'}
        return None

    def set_current_user_info_and_log(self, user):
        """
        Set the current user information and log the access.
        :param user: dict, the user information
        :return: None
        >>> filter = AccessGatewayFilter()
        >>> user = {'name': 'user1', 'address': '127.0.0.1'}
        >>> filter.set_current_user_info_and_log(user)

        """
        # Here you would typically set the current user information in a thread-local storage or a similar mechanism.
        # For simplicity, we will just log the user information.
        self.logger.info(
            f"User {user['name']} accessed the system at {datetime.now()}")
        # In a real application, you would also log the access details, such as the request URI, method, etc.


# Example usage:
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    filter = AccessGatewayFilter()
    request = {'path': '/api/data', 'method': 'GET', 'headers': {'Authorization': {
        'user': {'name': 'user1'}, 'jwt': 'user1'+str(datetime.now())}}}
    if filter.filter(request):
        print("Request allowed")
    else:
        print("Request denied")
