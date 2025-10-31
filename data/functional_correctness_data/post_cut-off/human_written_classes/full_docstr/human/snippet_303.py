from archipy.models.types import KeycloakErrorMessageType
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakConnectionError, KeycloakError, KeycloakGetError
from archipy.models.errors import ClientAlreadyExistsError, ConnectionTimeoutError, InsufficientPermissionsError, InternalError, InvalidCredentialsError, InvalidTokenError, KeycloakConnectionTimeoutError, KeycloakServiceUnavailableError, PasswordPolicyError, RealmAlreadyExistsError, ResourceNotFoundError, RoleAlreadyExistsError, UnauthenticatedError, UnavailableError, UserAlreadyExistsError, ValidationError
import json

class KeycloakExceptionHandlerMixin:
    """Mixin class to handle Keycloak exceptions in a consistent way."""

    @classmethod
    def _extract_error_message(cls, exception: KeycloakError) -> str:
        """Extract the actual error message from Keycloak error response.

        Args:
            exception: The Keycloak exception

        Returns:
            str: The extracted error message
        """
        error_message = str(exception)
        if hasattr(exception, 'response_body') and exception.response_body:
            try:
                body = exception.response_body
                if isinstance(body, bytes):
                    body_str = body.decode('utf-8')
                elif isinstance(body, str):
                    body_str = body
                else:
                    body_str = str(body)
                parsed = json.loads(body_str)
                if isinstance(parsed, dict):
                    error_message = parsed.get('errorMessage') or parsed.get('error_description') or parsed.get('error') or error_message
            except (json.JSONDecodeError, UnicodeDecodeError):
                pass
        return error_message

    @classmethod
    def _handle_keycloak_exception(cls, exception: KeycloakError, operation: str) -> None:
        """Handle Keycloak exceptions and map them to appropriate application errors.

        Args:
            exception: The original Keycloak exception
            operation: The name of the operation that failed

        Raises:
            Various application-specific errors based on the exception type/content
        """
        error_message = cls._extract_error_message(exception)
        response_code = getattr(exception, 'response_code', None)
        error_lower = error_message.lower()
        additional_data = {'operation': operation, 'original_error': error_message, 'response_code': response_code, 'keycloak_error_type': type(exception).__name__}
        if isinstance(exception, KeycloakConnectionError):
            if 'timeout' in error_lower:
                raise KeycloakConnectionTimeoutError(error=KeycloakErrorMessageType.CONNECTION_TIMEOUT.value, additional_data=additional_data) from exception
            raise KeycloakServiceUnavailableError(error=KeycloakErrorMessageType.SERVICE_UNAVAILABLE.value, additional_data=additional_data) from exception
        if isinstance(exception, KeycloakAuthenticationError) or any((phrase in error_lower for phrase in ['invalid user credentials', 'invalid credentials', 'authentication failed', 'unauthorized'])):
            raise InvalidCredentialsError(error=KeycloakErrorMessageType.INVALID_CREDENTIALS.value, additional_data=additional_data) from exception
        if 'already exists' in error_lower:
            if 'realm' in error_lower:
                raise RealmAlreadyExistsError(error=KeycloakErrorMessageType.REALM_ALREADY_EXISTS.value, additional_data=additional_data) from exception
            elif 'user exists with same' in error_lower:
                raise UserAlreadyExistsError(error=KeycloakErrorMessageType.USER_ALREADY_EXISTS.value, additional_data=additional_data) from exception
            elif 'client' in error_lower:
                raise ClientAlreadyExistsError(error=KeycloakErrorMessageType.CLIENT_ALREADY_EXISTS.value, additional_data=additional_data) from exception
            elif 'role' in error_lower:
                raise RoleAlreadyExistsError(error=KeycloakErrorMessageType.ROLE_ALREADY_EXISTS.value, additional_data=additional_data) from exception
        if 'not found' in error_lower:
            raise ResourceNotFoundError(error=KeycloakErrorMessageType.RESOURCE_NOT_FOUND.value, additional_data=additional_data) from exception
        if any((phrase in error_lower for phrase in ['forbidden', 'access denied', 'insufficient permissions', 'insufficient scope'])):
            raise InsufficientPermissionsError(error=KeycloakErrorMessageType.INSUFFICIENT_PERMISSIONS.value, additional_data=additional_data) from exception
        if any((phrase in error_lower for phrase in ['invalid password', 'password policy', 'minimum length', 'password must'])):
            raise PasswordPolicyError(error=KeycloakErrorMessageType.PASSWORD_POLICY_VIOLATION.value, additional_data=additional_data) from exception
        if response_code == 400 or any((phrase in error_lower for phrase in ['validation', 'invalid', 'required field', 'bad request'])):
            raise ValidationError(error=KeycloakErrorMessageType.VALIDATION_ERROR.value, additional_data=additional_data) from exception
        if response_code in [503, 504] or 'unavailable' in error_lower:
            raise KeycloakServiceUnavailableError(error=KeycloakErrorMessageType.SERVICE_UNAVAILABLE.value, additional_data=additional_data) from exception
        raise InternalError(additional_data=additional_data) from exception

    @classmethod
    def _handle_realm_exception(cls, exception: KeycloakError, operation: str, realm_name: str | None=None) -> None:
        """Handle realm-specific exceptions.

        Args:
            exception: The original Keycloak exception
            operation: The name of the operation that failed
            realm_name: The realm name involved in the operation

        Raises:
            RealmAlreadyExistsError: If realm already exists
            Various other errors from _handle_keycloak_exception
        """
        error_message = cls._extract_error_message(exception)
        if realm_name and 'already exists' in error_message.lower():
            additional_data = {'operation': operation, 'realm_name': realm_name, 'original_error': error_message, 'response_code': getattr(exception, 'response_code', None)}
            raise RealmAlreadyExistsError(error=KeycloakErrorMessageType.REALM_ALREADY_EXISTS.value, additional_data=additional_data) from exception
        cls._handle_keycloak_exception(exception, operation)

    @classmethod
    def _handle_user_exception(cls, exception: KeycloakError, operation: str, user_data: dict | None=None) -> None:
        """Handle user-specific exceptions.

        Args:
            exception: The original Keycloak exception
            operation: The name of the operation that failed
            user_data: The user data involved in the operation

        Raises:
            UserAlreadyExistsError: If user already exists
            Various other errors from _handle_keycloak_exception
        """
        error_message = cls._extract_error_message(exception)
        if 'user exists with same' in error_message.lower():
            additional_data = {'operation': operation, 'original_error': error_message, 'response_code': getattr(exception, 'response_code', None)}
            if user_data:
                additional_data.update({'username': user_data.get('username'), 'email': user_data.get('email')})
            raise UserAlreadyExistsError(error=KeycloakErrorMessageType.USER_ALREADY_EXISTS.value, additional_data=additional_data) from exception
        cls._handle_keycloak_exception(exception, operation)

    @classmethod
    def _handle_client_exception(cls, exception: KeycloakError, operation: str, client_data: dict | None=None) -> None:
        """Handle client-specific exceptions.

        Args:
            exception: The original Keycloak exception
            operation: The name of the operation that failed
            client_data: The client data involved in the operation

        Raises:
            ClientAlreadyExistsError: If client already exists
            Various other errors from _handle_keycloak_exception
        """
        error_message = cls._extract_error_message(exception)
        if 'client' in error_message.lower() and 'already exists' in error_message.lower():
            additional_data = {'operation': operation, 'original_error': error_message, 'response_code': getattr(exception, 'response_code', None)}
            if client_data:
                additional_data.update({'client_id': client_data.get('clientId'), 'client_name': client_data.get('name')})
            raise ClientAlreadyExistsError(error=KeycloakErrorMessageType.CLIENT_ALREADY_EXISTS.value, additional_data=additional_data) from exception
        cls._handle_keycloak_exception(exception, operation)