from typing import Optional, Dict, Any
from google.auth.credentials import Credentials
from google.auth import default as google_auth_default, impersonated_credentials
from google.oauth2 import service_account
# Assuming ChronicleClient is defined in .chronicle
from .chronicle import ChronicleClient


class SecOpsClient:
    '''Main client class for interacting with Google SecOps.'''

    def __init__(
        self,
        credentials: Optional[Credentials] = None,
        service_account_path: Optional[str] = None,
        service_account_info: Optional[Dict[str, Any]] = None,
        impersonate_service_account: Optional[str] = None,
    ):
        '''Initialize the SecOps client.
        Args:
            credentials: Optional pre-existing Google Auth credentials
            service_account_path: Optional path to service account JSON key file
            service_account_info: Optional service account JSON key data as dict
            impersonate_service_account: Optional service account to impersonate
        '''
        self._base_credentials = None

        if credentials is not None:
            self._base_credentials = credentials
        elif service_account_path is not None:
            self._base_credentials = service_account.Credentials.from_service_account_file(
                service_account_path
            )
        elif service_account_info is not None:
            self._base_credentials = service_account.Credentials.from_service_account_info(
                service_account_info
            )
        else:
            self._base_credentials, _ = google_auth_default()

        if impersonate_service_account:
            self._credentials = impersonated_credentials.Credentials(
                source_credentials=self._base_credentials,
                target_principal=impersonate_service_account,
                target_scopes=[
                    'https://www.googleapis.com/auth/cloud-platform'],
            )
        else:
            self._credentials = self._base_credentials

    def chronicle(
        self,
        customer_id: str,
        project_id: str,
        region: str = 'us'
    ) -> 'ChronicleClient':
        '''Get Chronicle API client.
        Args:
            customer_id: Chronicle customer ID
            project_id: GCP project ID
            region: Chronicle API region (default: "us")
        Returns:
            ChronicleClient instance
        '''
        return ChronicleClient(
            credentials=self._credentials,
            customer_id=customer_id,
            project_id=project_id,
            region=region
        )
