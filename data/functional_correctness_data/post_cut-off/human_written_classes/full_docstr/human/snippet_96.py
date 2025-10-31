from ultralytics.utils import IS_COLAB, LOGGER, SETTINGS, emojis
from ultralytics.hub.utils import HUB_API_ROOT, HUB_WEB_ROOT, PREFIX, request_with_credentials
import requests

class Auth:
    """
    Manages authentication processes including API key handling, cookie-based authentication, and header generation.

    The class supports different methods of authentication:
    1. Directly using an API key.
    2. Authenticating using browser cookies (specifically in Google Colab).
    3. Prompting the user to enter an API key.

    Attributes:
        id_token (str or bool): Token used for identity verification, initialized as False.
        api_key (str or bool): API key for authentication, initialized as False.
        model_key (bool): Placeholder for model key, initialized as False.
    """
    id_token = api_key = model_key = False

    def __init__(self, api_key='', verbose=False):
        """
        Initialize Auth class and authenticate user.

        Handles API key validation, Google Colab authentication, and new key requests. Updates SETTINGS upon successful
        authentication.

        Args:
            api_key (str): API key or combined key_id format.
            verbose (bool): Enable verbose logging.
        """
        api_key = api_key.split('_')[0]
        self.api_key = api_key or SETTINGS.get('api_key', '')
        if self.api_key:
            if self.api_key == SETTINGS.get('api_key'):
                if verbose:
                    LOGGER.info(f'{PREFIX}Authenticated ✅')
                return
            else:
                success = self.authenticate()
        elif IS_COLAB:
            success = self.auth_with_cookies()
        else:
            success = self.request_api_key()
        if success:
            SETTINGS.update({'api_key': self.api_key})
            if verbose:
                LOGGER.info(f'{PREFIX}New authentication successful ✅')
        elif verbose:
            LOGGER.info(f"{PREFIX}Get API key from {API_KEY_URL} and then run 'yolo login API_KEY'")

    def request_api_key(self, max_attempts=3):
        """
        Prompt the user to input their API key.

        Returns the model ID.
        """
        import getpass
        for attempts in range(max_attempts):
            LOGGER.info(f'{PREFIX}Login. Attempt {attempts + 1} of {max_attempts}')
            input_key = getpass.getpass(f'Enter API key from {API_KEY_URL} ')
            self.api_key = input_key.split('_')[0]
            if self.authenticate():
                return True
        raise ConnectionError(emojis(f'{PREFIX}Failed to authenticate ❌'))

    def authenticate(self) -> bool:
        """
        Attempt to authenticate with the server using either id_token or API key.

        Returns:
            (bool): True if authentication is successful, False otherwise.
        """
        try:
            if (header := self.get_auth_header()):
                r = requests.post(f'{HUB_API_ROOT}/v1/auth', headers=header)
                if not r.json().get('success', False):
                    raise ConnectionError('Unable to authenticate.')
                return True
            raise ConnectionError('User has not authenticated locally.')
        except ConnectionError:
            self.id_token = self.api_key = False
            LOGGER.warning(f'{PREFIX}Invalid API key ⚠️')
            return False

    def auth_with_cookies(self) -> bool:
        """
        Attempt to fetch authentication via cookies and set id_token. User must be logged in to HUB and running in a
        supported browser.

        Returns:
            (bool): True if authentication is successful, False otherwise.
        """
        if not IS_COLAB:
            return False
        try:
            authn = request_with_credentials(f'{HUB_API_ROOT}/v1/auth/auto')
            if authn.get('success', False):
                self.id_token = authn.get('data', {}).get('idToken', None)
                self.authenticate()
                return True
            raise ConnectionError('Unable to fetch browser authentication details.')
        except ConnectionError:
            self.id_token = False
            return False

    def get_auth_header(self):
        """
        Get the authentication header for making API requests.

        Returns:
            (dict): The authentication header if id_token or API key is set, None otherwise.
        """
        if self.id_token:
            return {'authorization': f'Bearer {self.id_token}'}
        elif self.api_key:
            return {'x-api-key': self.api_key}