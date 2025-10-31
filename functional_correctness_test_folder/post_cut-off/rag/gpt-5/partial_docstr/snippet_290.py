from typing import Any, Dict, Optional, TYPE_CHECKING

# Optional runtime-friendly imports to avoid hard dependency when not needed
try:
    from google.auth.credentials import Credentials as _GoogleCredentials  # type: ignore
    from google.oauth2 import service_account as _service_account  # type: ignore
    from google.auth import default as _google_auth_default  # type: ignore
    from google.auth.transport.requests import AuthorizedSession as _AuthorizedSession  # type: ignore
    from google.auth.impersonated_credentials import Credentials as _ImpersonatedCredentials  # type: ignore
except Exception:  # pragma: no cover
    _GoogleCredentials = None
    _service_account = None
    _google_auth_default = None
    _AuthorizedSession = None
    _ImpersonatedCredentials = None


if TYPE_CHECKING:
    from google.auth.credentials import Credentials  # type: ignore
else:
    # Fallback minimal stub to satisfy annotations at runtime when google-auth not installed
    class Credentials:  # type: ignore
        pass


class ChronicleClient:
    def __init__(self, credentials: Optional[Credentials], customer_id: str, project_id: str, region: str = "us"):
        self.credentials = credentials
        self.customer_id = customer_id
        self.project_id = project_id
        self.region = region
        self.base_url = self._build_base_url(region)
        self.session = _AuthorizedSession(credentials) if (
            _AuthorizedSession and credentials) else None

    @staticmethod
    def _build_base_url(region: str) -> str:
        r = (region or "us").strip().lower()
        if r.startswith("http://") or r.startswith("https://"):
            return r.rstrip("/")
        if "." in r:
            return f"https://{r}".rstrip("/")
        return f"https://{r}-chronicle.googleapis.com"


class SecOpsClient:
    '''Main client class for interacting with Google SecOps.'''

    DEFAULT_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(self, credentials: Optional[Credentials] = None, service_account_path: Optional[str] = None, service_account_info: Optional[Dict[str, Any]] = None, impersonate_service_account: Optional[str] = None):
        '''Initialize the SecOps client.
        Args:
            credentials: Optional pre-existing Google Auth credentials
            service_account_path: Optional path to service account JSON key file
            service_account_info: Optional service account JSON key data as dict
            impersonate_service_account: Optional service account to impersonate
        '''
        if credentials is not None and not isinstance(credentials, Credentials):
            raise TypeError(
                "credentials must be a google.auth.credentials.Credentials instance")

        if service_account_path and service_account_info:
            raise ValueError(
                "Provide either service_account_path or service_account_info, not both")

        source_credentials: Optional[Credentials] = credentials

        if source_credentials is None and (service_account_path or service_account_info):
            if not _service_account:  # pragma: no cover
                raise ImportError(
                    "google-auth is required for service account credentials")
            if service_account_path:
                source_credentials = _service_account.Credentials.from_service_account_file(
                    service_account_path, scopes=self.DEFAULT_SCOPES)  # type: ignore
            else:
                source_credentials = _service_account.Credentials.from_service_account_info(
                    service_account_info, scopes=self.DEFAULT_SCOPES)  # type: ignore

        if source_credentials is None:
            if not _google_auth_default:  # pragma: no cover
                raise ImportError(
                    "google-auth is required to obtain default credentials")
            source_credentials, _ = _google_auth_default(
                scopes=self.DEFAULT_SCOPES)  # type: ignore

        final_credentials: Credentials = source_credentials

        if impersonate_service_account:
            if not _ImpersonatedCredentials:  # pragma: no cover
                raise ImportError(
                    "google-auth is required for service account impersonation")
            final_credentials = _ImpersonatedCredentials(  # type: ignore
                source_credentials=source_credentials,
                target_principal=impersonate_service_account,
                target_scopes=list(self.DEFAULT_SCOPES),
                lifetime=3600,
            )

        self.source_credentials: Credentials = source_credentials  # type: ignore
        self.credentials: Credentials = final_credentials  # type: ignore

    def chronicle(self, customer_id: str, project_id: str, region: str = 'us') -> ChronicleClient:
        '''Get Chronicle API client.
        Args:
            customer_id: Chronicle customer ID
            project_id: GCP project ID
            region: Chronicle API region (default: "us")
        Returns:
            ChronicleClient instance
        '''
        return ChronicleClient(self.credentials, customer_id=customer_id, project_id=project_id, region=region)
