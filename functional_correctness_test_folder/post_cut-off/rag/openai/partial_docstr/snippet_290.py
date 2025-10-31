
from __future__ import annotations

from typing import Any, Dict, Optional

import google.auth
from google.oauth2 import service_account
from google.auth import impersonated_credentials

# The ChronicleClient is expected to be defined elsewhere in the package.
# Import it here; adjust the import path if necessary.
try:
    from .chronicle import ChronicleClient
except Exception:  # pragma: no cover
    # Fallback: define a minimal placeholder for type checking / documentation.
    class ChronicleClient:  # type: ignore
        def __init__(self, *_, **__):
            raise NotImplementedError(
                "ChronicleClient is not available in this environment.")


class SecOpsClient:
    """Main client class for interacting with Google SecOps."""

    def __init__(
        self,
        credentials: Optional[Any] = None,
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
        # Resolve base credentials
        if credentials is not None:
            base_credentials = credentials
        elif service_account_path is not None:
            base_credentials = service_account.Credentials.from_service_account_file(
                service_account_path
            )
        elif service_account_info is not None:
            base_credentials = service_account.Credentials.from_service_account_info(
                service_account_info
            )
        else:
            base_credentials, _ = google.auth.default()

        # Handle impersonation if requested
        if impersonate_service_account:
            # Impersonation requires a service account file or info
            if service_account_path is not None:
                self.credentials = impersonated_credentials.Credentials.from_service_account_file(
                    service_account_path,
                    target_principal=impersonate_service_account,
                    scopes=base_credentials.scopes or [
                        "https://www.googleapis.com/auth/cloud-platform"],
                )
            elif service_account_info is not None:
                self.credentials = impersonated_credentials.Credentials.from_service_account_info(
                    service_account_info,
                    target_principal=impersonate_service_account,
                    scopes=base_credentials.scopes or [
                        "https://www.googleapis.com/auth/cloud-platform"],
                )
            else:
                raise ValueError(
                    "Impersonation requires a service account file or info."
                )
        else:
            self.credentials = base_credentials

        # Store optional parameters for potential future use
        self.service_account_path = service_account_path
        self.service_account_info = service_account_info
        self.impersonate_service_account = impersonate_service_account

    def chronicle(
        self,
        customer_id: str,
        project_id: str,
        region: str = "us",
    ) -> ChronicleClient:
        """
        Get Chronicle API client.

        Args:
            customer_id: Chronicle customer ID.
            project_id: GCP project ID.
            region: Chronicle API region (default: "us").

        Returns:
            ChronicleClient instance.
        """
        return ChronicleClient(
            credentials=self.credentials,
            customer_id=customer_id,
            project_id=project_id,
