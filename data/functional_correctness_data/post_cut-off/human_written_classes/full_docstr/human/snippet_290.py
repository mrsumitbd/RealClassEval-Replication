from secops.chronicle import ChronicleClient
from typing import Optional, Dict, Any
from secops.auth import SecOpsAuth
from google.auth.credentials import Credentials

class SecOpsClient:
    """Main client class for interacting with Google SecOps."""

    def __init__(self, credentials: Optional[Credentials]=None, service_account_path: Optional[str]=None, service_account_info: Optional[Dict[str, Any]]=None, impersonate_service_account: Optional[str]=None):
        """Initialize the SecOps client.

        Args:
            credentials: Optional pre-existing Google Auth credentials
            service_account_path: Optional path to service account JSON key file
            service_account_info: Optional service account JSON key data as dict
            impersonate_service_account: Optional service account to impersonate
        """
        self.auth = SecOpsAuth(credentials=credentials, service_account_path=service_account_path, service_account_info=service_account_info, impersonate_service_account=impersonate_service_account)
        self._chronicle = None

    def chronicle(self, customer_id: str, project_id: str, region: str='us') -> ChronicleClient:
        """Get Chronicle API client.

        Args:
            customer_id: Chronicle customer ID
            project_id: GCP project ID
            region: Chronicle API region (default: "us")

        Returns:
            ChronicleClient instance
        """
        return ChronicleClient(customer_id=customer_id, project_id=project_id, region=region, auth=self.auth)