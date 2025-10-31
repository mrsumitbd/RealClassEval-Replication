
from __future__ import annotations

from typing import Any, Dict, Optional

# Google auth imports
import google.auth
from google.oauth2 import service_account
from google.auth import impersonated_credentials

# Assume ChronicleClient is defined elsewhere in the package
# from .chronicle import ChronicleClient
# For the purpose of this implementation we will import it lazily


def _import_chronicle_client():
    from .chronicle import ChronicleClient  # type: ignore
    return ChronicleClient


class SecOpsClient:
    """Main client class for interacting with Google SecOps."""

    def __init__(
        self,
        credentials: Optional[google.auth.credentials.Credentials] = None,
        service_account_path: Optional[str] = None,
        service_account_info: Optional[Dict[str, Any]] = None,
        impersonate_service_account: Optional[str] = None,
    ):
        """
        Initialize the SecOps client.

        Args:
            credentials: Optional pre-existing Google Auth credentials.
            service_account_path: Optional path to service account JSON key file.
            service_account_info: Optional service account JSON key data as dict.
            impersonate_service_account: Optional service account to impersonate.
        """
        # Validate mutually exclusive inputs
        if credentials and (service_account_path or service_account_info):
            raise ValueError(
                "Provide either `credentials` or a service account source, not both."
            )

        # Load credentials from service account file or dict
        if service_account_path or service_account_info:
            if service_account_path:
                source_creds = service_account.Credentials.from_service_account_file(
                    service_account_path
                )
            else:
                source_creds = service_account.Credentials.from_service_account_info(
                    service_account_info
                )

            # If impersonation requested, wrap the source credentials
            if impersonate_service_account:
                # Default scopes for SecOps APIs
                scopes = ["https://www.googleapis.com/auth/cloud-platform"]
                self.credentials = impersonated_credentials.Credentials(
                    source_credentials=source_creds,
                    target_principal=impersonate_service_account,
                    scopes=scopes,
                )
            else:
                self.credentials = source_creds
        else:
            # No explicit credentials provided – fall back to default
            if credentials:
                self.credentials = credentials
            else:
                # Use application default credentials
                self.credentials, _ = google.auth.default()

    def chronicle(
        self,
        customer_id: str,
        project_id: str,
        region: str = "us",
    ) -> "ChronicleClient":
        """
        Get Chronicle API client.

        Args:
            customer_id: Chronicle customer ID.
            project_id: GCP project ID.
            region: Chronicle API region (default: "us").

        Returns:
            ChronicleClient instance.
        """
        ChronicleClient = _import_chronicle_client()
        return ChronicleClient(
            credentials=self.credentials,
            customer_id=customer_id,
            project_id=project_id,
            region=region,
        )
