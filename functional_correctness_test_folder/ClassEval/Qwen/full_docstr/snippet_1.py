
import datetime


class AccessGatewayFilter:
    """
    This class is a filter used for accessing gateway filtering, primarily for authentication and access log recording.
    """

    def __init__(self):
        pass

    def filter(self, request):
        """
        Filter the incoming request based on certain rules and conditions.
        :param request: dict, the incoming request details
        :return: bool, True if the request is allowed, False otherwise
        """
        request_uri = request.get('path', '')
        if self.is_start_with(request_uri):
            user = self.get_jwt_user(request)
            if user:
                self.set_current_user_info_and_log(user)
                return True
        return False

    def is_start_with(self, request_uri):
        """
        Check if the request URI starts with certain prefixes.
        Currently, the prefixes being checked are "/api" and "/login".
        :param request_uri: str, the URI of the request
        :return: bool, True if the URI starts with certain prefixes, False otherwise
        """
        return request_uri.startswith('/api') or request_uri.startswith('/login')

    def get_jwt_user(self, request):
        """
        Get the user information from the JWT token in the request.
        :param request: dict, the incoming request details
        :return: dict or None, the user information if the token is valid, None otherwise
        """
        auth_header = request.get('headers', {}).get('Authorization', {})
        jwt_token = auth_header.get('jwt')
        user_info = auth_header.get('user')
        if jwt_token and user_info:
            # Here we assume the JWT token is valid if it contains the user's name and today's date
            expected_token = user_info['name'] + str(datetime.date.today())
            if jwt_token == expected_token:
                return user_info
        return None

    def set_current_user_info_and_log(self, user):
        """
        Set the current user information and log the access.
        :param user: dict, the user information
        :return: None
        """
        # This is a placeholder for setting user info and logging
        print(
            f"User {user['name']} from {user['address']} accessed the system.")
