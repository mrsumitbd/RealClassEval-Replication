
from typing import Dict, Any, Optional
from google.auth.credentials import Credentials
from google.oauth2 import service_account


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
        if credentials:
            self.credentials = credentials
        elif service_account_path:
            self.credentials = service_account.Credentials.from_service_account_file(
                service_account_path,
                scopes=['https://www.googleapis.com/auth/chronicle-backstory'],
                subject=impersonate_service_account
            )
        elif service_account_info:
            self.credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=['https://www.googleapis.com/auth/chronicle-backstory'],
                subject=impersonate_service_account
            )
        else:
            raise ValueError(
                "Either credentials, service_account_path, or service_account_info must be provided")

    def chronicle(self, customer_id: str, project_id: str, region: str = 'us') -> ChronicleClient:
        '''Get Chronicle API client.
        Args:
            customer_id: Chronicle customer ID
            project_id: GCP project ID
            region: Chronicle API region (default: "us")
        Returns:
            ChronicleClient instance
        '''
        return ChronicleClient(
            credentials=self.credentials,
            customer_id=customer_id,
            project_id=project_id,
            region=region
        )
