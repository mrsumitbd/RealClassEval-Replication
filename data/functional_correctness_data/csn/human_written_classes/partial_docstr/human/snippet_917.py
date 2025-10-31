from oic.utils.settings import ClientSettings
from oic.oic import Client
import requests

class ProviderConfiguration:
    """
    Metadata for communicating with an OpenID Connect Provider (OP).

    Attributes:
        auth_request_params (dict): Extra parameters, as key-value pairs, to include in the query parameters
            of the authentication request
        registered_client_metadata (ClientMetadata): The client metadata registered with the provider.
        requests_session (requests.Session): Requests object to use when communicating with the provider.
        session_refresh_interval_seconds (int): Number of seconds between updates of user data (tokens, user data, etc.)
            fetched from the provider. If `None` is specified, no silent updates should be made user data will be made.
        userinfo_endpoint_method (str): HTTP method ("GET" or "POST") to use when making the UserInfo Request. If
            `None` is specified, no UserInfo Request will be made.
    """
    DEFAULT_REQUEST_TIMEOUT = 5

    def __init__(self, issuer=None, provider_metadata=None, userinfo_http_method='GET', client_registration_info=None, client_metadata=None, auth_request_params=None, session_refresh_interval_seconds=None, requests_session=None):
        """
        Args:
            issuer (str): OP Issuer Identifier. If this is specified discovery will be used to fetch the provider
                metadata, otherwise `provider_metadata` must be specified.
            provider_metadata (ProviderMetadata): OP metadata,
            userinfo_http_method (Optional[str]): HTTP method (GET or POST) to use when sending the UserInfo Request.
                If `none` is specified, no userinfo request will be sent.
            client_registration_info (ClientRegistrationInfo): Client metadata to register your app
                dynamically with the provider. Either this or `registered_client_metadata` must be specified.
            client_metadata (ClientMetadata): Client metadata if your app is statically
                registered with the provider. Either this or `client_registration_info` must be specified.
            auth_request_params (dict): Extra parameters that should be included in the authentication request.
            session_refresh_interval_seconds (int): Length of interval (in seconds) between attempted user data
                refreshes.
            requests_session (requests.Session): custom requests object to allow for example retry handling, etc.
        """
        if not issuer and (not provider_metadata):
            raise ValueError("Specify either 'issuer' or 'provider_metadata'.")
        if not client_registration_info and (not client_metadata):
            raise ValueError("Specify either 'client_registration_info' or 'client_metadata'.")
        self._issuer = issuer
        self._provider_metadata = provider_metadata
        self._client_registration_info = client_registration_info
        self._client_metadata = client_metadata
        self.userinfo_endpoint_method = userinfo_http_method
        self.auth_request_params = auth_request_params or {}
        self.session_refresh_interval_seconds = session_refresh_interval_seconds
        self.client_settings = ClientSettings(timeout=self.DEFAULT_REQUEST_TIMEOUT, requests_session=requests_session or requests.Session())

    def ensure_provider_metadata(self, client: Client):
        if not self._provider_metadata:
            resp = client.provider_config(self._issuer)
            logger.debug(f'Received discovery response: {resp.to_dict()}')
            self._provider_metadata = ProviderMetadata(**resp.to_dict())
        return self._provider_metadata

    @property
    def registered_client_metadata(self):
        return self._client_metadata

    def register_client(self, client: Client):
        if not self._client_metadata:
            if not self._provider_metadata['registration_endpoint']:
                raise ValueError("Can't use dynamic client registration, provider metadata is missing 'registration_endpoint'.")
            registration_request = self._client_registration_info.to_dict()
            registration_response = client.register(url=self._provider_metadata['registration_endpoint'], **registration_request)
            logger.info('Received registration response.')
            self._client_metadata = ClientMetadata(**registration_response.to_dict())
        return self._client_metadata