from typing import Any
from users import User

class AuthFactory:
    """
    Factory class for creating authentication tokens or objects.
    """

    @staticmethod
    def create_symmetric_jwt_token_for_user(user: User, jwt_key: str) -> str:
        if not user:
            raise ValueError('User is required to create a symmetric JWT token.')
        if not str(jwt_key):
            raise ValueError('JWT key is required to create a symmetric JWT token.')
        jwt_payload = JwtPayload(subject=user.id, name=user.name, roles=user.roles)
        symmetric_jwt = SymmetricJwtToken(jwt_key, jwt_payload)
        return symmetric_jwt.encode()

    @staticmethod
    def create_jwt_payload_for_user(user: User) -> Any:
        """
        Create a JWT payload from a User object.

        Args:
            user (User): The user object to create the payload from.

        Returns:
            Any: A dictionary representing the JWT payload.
        """
        if not user:
            raise ValueError('User is required to create JWT payload.')
        return {'sub': user.id, 'name': user.name, 'roles': user.roles}