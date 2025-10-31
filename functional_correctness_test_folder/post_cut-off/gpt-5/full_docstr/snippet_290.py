from typing import Optional, Dict, Any

# Try to import Google Auth types and factories; provide graceful fallbacks if unavailable.
try:
    from google.auth.credentials import Credentials  # type: ignore
except Exception:
    class Credentials:  # minimal placeholder for type hints
        def with_scopes(self, scopes):
            return self

try:
    import google.auth
except Exception:
    google = None  # type: ignore

try:
    from google.oauth2 import service_account  # type: ignore
except Exception:
    service_account = None  # type: ignore

try:
    from google.auth import impersonated_credentials  # type: ignore
except Exception:
    impersonated_credentials = None  # type: ignore


DEFAULT_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)


class ChronicleClient:
    def __init__(self, credentials: Credentials, customer_id: str, project_id: str, region: str = "us"):
        self.credentials = credentials
        self.customer_id = customer_id
        self.project_id = project_id
        self.region = region

    def __repr__(self):
        return (
            f"ChronicleClient(customer_id={self.customer_id!r}, "
            f"project_id={self.project_id!r}, region={self.region!r})"
        )


class SecOpsClient:
    '''Main client class for interacting with Google SecOps.'''

    def __init__(self, credentials: Optional[Credentials] = None, service_account_path: Optional[str] = None,
                 service_account_info: Optional[Dict[str, Any]] = None, impersonate_service_account: Optional[str] = None):
        '''Initialize the SecOps client.
        Args:
            credentials: Optional pre-existing Google Auth credentials
            service_account_path: Optional path to service account JSON key file
            service_account_info: Optional service account JSON key data as dict
            impersonate_service_account: Optional service account to impersonate
        '''
        creds: Optional[Credentials] = None

        if credentials is not None:
            creds = credentials

        elif service_account_info is not None:
            if service_account is None:
                raise RuntimeError(
                    "google.oauth2.service_account is required to use service_account_info")
            creds = service_account.Credentials.from_service_account_info(
                service_account_info, scopes=DEFAULT_SCOPES)

        elif service_account_path is not None:
            if service_account is None:
                raise RuntimeError(
                    "google.oauth2.service_account is required to use service_account_path")
            creds = service_account.Credentials.from_service_account_file(
                service_account_path, scopes=DEFAULT_SCOPES)

        else:
            if google is None:
                raise RuntimeError(
                    "google.auth is not available and no credentials or service account info/path were provided"
                )
            creds, _ = google.auth.default(scopes=DEFAULT_SCOPES)

        if impersonate_service_account:
            if impersonated_credentials is None:
                raise RuntimeError(
                    "google.auth.impersonated_credentials is required for impersonation")
            # Ensure base credentials have scopes for generating tokens
            base_creds = creds
            try:
                # Some credential types support with_scopes
                # type: ignore[attr-defined]
                base_creds = creds.with_scopes(DEFAULT_SCOPES)
            except Exception:
                pass
            creds = impersonated_credentials.Credentials(
                source_credentials=base_creds,
                target_principal=impersonate_service_account,
                target_scopes=list(DEFAULT_SCOPES),
                lifetime=3600,
            )

        self._credentials: Credentials = creds  # type: ignore[assignment]

    def chronicle(self, customer_id: str, project_id: str, region: str = 'us') -> ChronicleClient:
        '''Get Chronicle API client.
        Args:
            customer_id: Chronicle customer ID
            project_id: GCP project ID
            region: Chronicle API region (default: "us")
        Returns:
            ChronicleClient instance
        '''
        return ChronicleClient(credentials=self._credentials, customer_id=customer_id, project_id=project_id, region=region)
