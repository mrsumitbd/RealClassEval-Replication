
from typing import Any, Dict, Optional
from google.auth.credentials import Credentials
from google.oauth2 import service_account
from google.auth import impersonated_credentials


class SecOpsClient:
    '''Main client class for interacting with Google SecOps.'''

    def __init__(self, credentials: Optional[Credentials] = None, service_account_path: Optional[str] = None, service_account_info: Optional[Dict[str, Any]] = None, impersonate_service_account: Optional[str] = None):
        '''Initialize the SecOps client.
        Args:
            credentials: Optional pre-existing Google Auth credentials
            service_account_path: Optional path to service account JSON key file
            service_account_info: Optional service account JSON key data as dict
            impersonate_service_account: Optional service account to impersonate
        '''
        self.credentials = credentials
        self.service_account_path = service_account_path
        self.service_account_info = service_account_info
        self.impersonate_service_account = impersonate_service_account

        if not self.credentials:
            if self.service_account_path:
                self.credentials = service_account.Credentials.from_service_account_file(
                    self.service_account_path
                )
            elif self.service_account_info:
                self.credentials = service_account.Credentials.from_service_account_info(
                    self.service_account_info
                )

        if self.impersonate_service_account and self.credentials:
            self.credentials = impersonated_credentials.Credentials(
                source_credentials=self.credentials,
                target_principal=self.impersonate_service_account,
                target_scopes=[
                    'https://www.googleapis.com/auth/cloud-platform']
            )

    def chronicle(self, customer_id: str, project_id: str, region: str = 'us') -> 'ChronicleClient':
        '''Get Chronicle API client.
        Args:
            customer_id: Chronicle customer ID
            project_id: GCP project ID
            region: Chronicle API region (default: "us")
        Returns:
            ChronicleClient instance
        '''
        from .chronicle import ChronicleClient
        return ChronicleClient(
            credentials=self.credentials,
            customer_id=customer_id,
            project_id=project_id,
            region=region
        )
