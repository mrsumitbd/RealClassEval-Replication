import datetime
from typing import Any, Dict, List, Optional


class AccessGatewayFilter:
    """
    This class is a filter used for accessing gateway filtering, primarily for authentication and access log recording.
    """

    def __init__(self):
        self.allowed_prefixes = ("/api", "/login")
        self.current_user: Optional[Dict[str, Any]] = None
        self.access_log: List[Dict[str, Any]] = []

    def filter(self, request):
        """
        Filter the incoming request based on certain rules and conditions.
        :param request: dict, the incoming request details
        :return: bool, True if the request is allowed, False otherwise
        >>> filter = AccessGatewayFilter()
        >>> filter.filter({'path': '/login', 'method': 'POST'})
        True

        """
        if not isinstance(request, dict):
            return False

        path = request.get("path", "")
        method = request.get("method", "").upper()
        if not isinstance(path, str) or not path:
            return False

        if not self.is_start_with(path):
            return False

        if path.startswith("/login"):
            # Allow login endpoint (commonly POST). For simplicity allow any method on /login.
            self.set_current_user_info_and_log(
                {"name": "anonymous", "address": request.get("ip")})
            return True

        if path.startswith("/api"):
            user = self.get_jwt_user(request)
            if user is None:
                return False
            # On valid auth, set user and log
            flattened_user = user.get(
                "user") if isinstance(user, dict) else None
            if isinstance(flattened_user, dict):
                # include ip if present
                if request.get("ip"):
                    flattened_user = {**flattened_user,
                                      "address": request.get("ip")}
                self.set_current_user_info_and_log(flattened_user)
            else:
                self.set_current_user_info_and_log(
                    {"name": "unknown", "address": request.get("ip")})
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
        if not isinstance(request_uri, str):
            return False
        return any(request_uri.startswith(prefix) for prefix in self.allowed_prefixes)

    def get_jwt_user(self, request):
        """
        Get the user information from the JWT token in the request.
        :param request: dict, the incoming request details
        :return: dict or None, the user information if the token is valid, None otherwise
        >>> filter = AccessGatewayFilter()
        >>> filter.get_jwt_user({'headers': {'Authorization': {'user': {'name': 'user1'}, 'jwt': 'user1'+str(datetime.date.today())}}})
        {'user': {'name': 'user1'}

        """
        headers = {}
        if isinstance(request, dict):
            headers = request.get("headers") or {}

        auth = headers.get("Authorization")
        if isinstance(auth, dict):
            user_info = auth.get("user")
            token = auth.get("jwt")
            if isinstance(user_info, dict):
                name = user_info.get("name")
                if isinstance(name, str) and isinstance(token, str):
                    expected = f"{name}{datetime.date.today()}"
                    if token == expected:
                        return {"user": {"name": name}}
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
        if isinstance(user, dict):
            self.current_user = user
        else:
            self.current_user = None

        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "user": self.current_user,
        }
        self.access_log.append(entry)
