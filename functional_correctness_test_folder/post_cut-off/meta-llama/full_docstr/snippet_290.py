
from google.oauth2 import service_account
from google.auth import default, impersonated_credentials
from google.auth.credentials import Credentials
from typing import Optional, Dict, Any


class ChronicleClient:
    # Assuming ChronicleClient is defined elsewhere
    pass


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
                service_account_path)
        elif service_account_info:
            self.credentials = service_account.Credentials.from_service_account_info(
                service_account_info)
        else:
            self.credentials, _ = default(
                scopes=['https://www.googleapis.com/auth/cloud-platform'])

        if impersonate_service_account:
            self.credentials = impersonated_credentials.Credentials(
                source_credentials=self.credentials,
                target_principal=impersonate_service_account,
                target_scopes=[
                    'https://www.googleapis.com/auth/cloud-platform']
            )

    def chronicle(self, customer_id: str, project_id: str, region: str = 'us') -> ChronicleClient:
        '''Get Chronicle API client.
        Args:
            customer_id: Chronicle customer ID
            project_id: GCP project ID
            region: Chronicle API region (default: "us")
        Returns:
            ChronicleClient instance
        '''
        return ChronicleClient(self.credentials, customer_id, project_id, region)
