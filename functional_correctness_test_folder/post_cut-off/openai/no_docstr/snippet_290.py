
from typing import Optional, Dict, Any
import google.auth
from google.oauth2 import service_account
from google.auth import impersonated_credentials

# Assume ChronicleClient is defined elsewhere and imported here
from .chronicle_client import ChronicleClient  # Adjust import path as needed


class SecOpsClient:
    """
    Client for interacting with Google Cloud Security Operations services.
    """

    def __init__(
        self,
        credentials: Optional[google.auth.credentials.Credentials] = None,
        service_account_path: Optional[str] = None,
        service_account_info: Optional[Dict[str, Any]] = None,
        impersonate_service_account: Optional[str] = None,
    ):
        """
        Initialize the SecOpsClient.

        Parameters
        ----------
        credentials : Optional[google.auth.credentials.Credentials]
            Explicit credentials to use. If provided, other credential options are ignored.
        service_account_path : Optional[str]
            Path to a JSON service account key file.
        service_account_info : Optional[Dict[str, Any]]
            Dictionary containing service account key information.
        impersonate_service_account : Optional[str]
            Email of a service account to impersonate.
        """
        # Resolve credentials
        if credentials is not None:
            self._credentials = credentials
        elif service_account_path is not None:
            self._credentials = service_account.Credentials.from_service_account_file(
                service_account_path
            )
        elif service_account_info is not None:
            self._credentials = service_account.Credentials.from_service_account_info(
                service_account_info
            )
        else:
            self._credentials, _ = google.auth.default()

        # Impersonate if requested
        if impersonate_service_account:
            self._credentials = impersonated_credentials.Credentials(
                source_credentials=self._credentials,
                target_principal=impersonate_service_account,
                target_scopes=self._credentials.scopes,
                lifetime=3600,
            )

    def chronicle(
        self,
        customer_id: str,
        project_id: str,
        region: str = "us",
    ) -> ChronicleClient:
        """
        Create a ChronicleClient for the specified customer and project.

        Parameters
        ----------
        customer_id : str
            The customer ID for Chronicle.
        project_id : str
            The GCP project ID.
        region : str, default="us"
            The region for the Chronicle service.

        Returns
        -------
        ChronicleClient
            A configured Chronicle client instance.
        """
        return ChronicleClient(
            credentials=self._credentials,
            customer_id=customer_id,
            project_id=project_id,
            region=region,
        )
