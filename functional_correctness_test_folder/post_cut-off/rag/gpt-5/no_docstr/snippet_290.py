from typing import Any, Dict, Optional, TYPE_CHECKING

import google.auth
from google.auth.credentials import Credentials
from google.oauth2 import service_account

try:
    # Available in google-auth >= 2.14
    from google.auth.credentials import with_scopes_if_required as _with_scopes_if_required
except Exception:
    _with_scopes_if_required = None  # type: ignore

try:
    from google.auth.impersonated_credentials import Credentials as ImpersonatedCredentials
except Exception:
    ImpersonatedCredentials = None  # type: ignore


if TYPE_CHECKING:
    from .chronicle import ChronicleClient  # type: ignore


class SecOpsClient:
    '''Main client class for interacting with Google SecOps.'''

    DEFAULT_SCOPES = (
        'https://www.googleapis.com/auth/cloud-platform',
        'https://www.googleapis.com/auth/chronicle-backstory',
    )

    def __init__(self, credentials: Optional[Credentials] = None, service_account_path: Optional[str] = None, service_account_info: Optional[Dict[str, Any]] = None, impersonate_service_account: Optional[str] = None):
        '''Initialize the SecOps client.
        Args:
            credentials: Optional pre-existing Google Auth credentials
            service_account_path: Optional path to service account JSON key file
            service_account_info: Optional service account JSON key data as dict
            impersonate_service_account: Optional service account to impersonate
        '''
        if service_account_path and service_account_info:
            raise ValueError(
                'Provide only one of service_account_path or service_account_info')

        base_credentials: Optional[Credentials] = None
        project_id: Optional[str] = None

        if credentials is not None:
            base_credentials = credentials
        elif service_account_info is not None:
            base_credentials = service_account.Credentials.from_service_account_info(
                service_account_info)  # type: ignore[arg-type]
        elif service_account_path is not None:
            base_credentials = service_account.Credentials.from_service_account_file(
                service_account_path)
        else:
            base_credentials, project_id = google.auth.default()

        if base_credentials is None:
            raise ValueError(
                'Unable to determine base credentials for SecOpsClient')

        # Ensure scopes
        if _with_scopes_if_required:
            base_credentials = _with_scopes_if_required(
                base_credentials, self.DEFAULT_SCOPES)  # type: ignore[assignment]
        else:
            requires_scopes = getattr(
                base_credentials, 'requires_scopes', False)
            if requires_scopes and hasattr(base_credentials, 'with_scopes'):
                base_credentials = base_credentials.with_scopes(
                    self.DEFAULT_SCOPES)  # type: ignore[assignment]

        final_credentials: Credentials = base_credentials

        # Optional impersonation
        if impersonate_service_account:
            if ImpersonatedCredentials is None:
                raise RuntimeError(
                    'google-auth does not support impersonated credentials in this environment')
            final_credentials = ImpersonatedCredentials(
                source_credentials=base_credentials,
                target_principal=impersonate_service_account,
                target_scopes=list(self.DEFAULT_SCOPES),
                lifetime=3600,
            )

        self._credentials: Credentials = final_credentials
        self._project_id: Optional[str] = project_id

    def chronicle(self, customer_id: str, project_id: str, region: str = 'us') -> 'ChronicleClient':
        '''Get Chronicle API client.
        Args:
            customer_id: Chronicle customer ID
            project_id: GCP project ID
            region: Chronicle API region (default: "us")
        Returns:
            ChronicleClient instance
        '''
        try:
            from .chronicle import ChronicleClient  # type: ignore
        except Exception:
            try:
                from chronicle import ChronicleClient  # type: ignore
            except Exception as exc:
                raise ImportError(
                    'ChronicleClient is not available. Ensure the Chronicle client module is installed and importable.') from exc

        return ChronicleClient(
            credentials=self._credentials,
            customer_id=customer_id,
            project_id=project_id,
            region=region,
        )
