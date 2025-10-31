
import datetime


class AccessGatewayFilter:
    """
    This class is a filter used for accessing gateway filtering, primarily for authentication and access log recording.
    """

    def __init__(self):
        # You could initialize logs or user info here if needed
        self.current_user = None
        self.access_logs = []

    def filter(self, request):
        """
        Filter the incoming request based on certain rules and conditions.
        :param request: dict, the incoming request details
        :return: bool, True if the request is allowed, False otherwise
        >>> filter = AccessGatewayFilter()
        >>> filter.filter({'path': '/login', 'method': 'POST'})
        True

        """
        path = request.get('path', '')
        if self.is_start_with(path):
            return True
        user = self.get_jwt_user(request)
        if user:
            self.set_current_user_info_and_log(user.get('user', {}))
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
        prefixes = ['/api', '/login']
        return any(request_uri.startswith(prefix) for prefix in prefixes)

    def get_jwt_user(self, request):
        """
        Get the user information from the JWT token in the request.
        :param request: dict, the incoming request details
        :return: dict or None, the user information if the token is valid, None otherwise
        >>> filter = AccessGatewayFilter()
        >>> filter.get_jwt_user({'headers': {'Authorization': {'user': {'name': 'user1'}, 'jwt': 'user1'+str(datetime.date.today())}}})
        {'user': {'name': 'user1'}

        """
        headers = request.get('headers', {})
        auth = headers.get('Authorization', {})
        user = auth.get('user')
        jwt = auth.get('jwt')
        if user and jwt:
            # Simulate JWT validation: jwt == user['name'] + str(today)
            today = str(datetime.date.today())
            expected_jwt = user.get('name', '') + today
            if jwt == expected_jwt:
                return {'user': user}
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
        self.current_user = user
        log_entry = {
            'user': user,
            'timestamp': datetime.datetime.now().isoformat()
        }
        self.access_logs.append(log_entry)
