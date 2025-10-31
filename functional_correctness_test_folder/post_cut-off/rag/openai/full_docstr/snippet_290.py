
from __future__ import annotations

from typing import Any, Dict, Optional

# Google auth imports
from google.auth import credentials as _ga_credentials
from google.oauth2 import service_account
from google.auth.impersonated_credentials import Credentials as ImpersonatedCredentials
from google.auth.transport.requests import Request as _Request

# Assume ChronicleClient is defined elsewhere in the package
try:
    from .chronicle import ChronicleClient
except Exception:  # pragma: no cover
    # Fallback stub for type checking / documentation purposes
    class ChronicleClient:  # type: ignore
        def __init__(self, *_, **__):
            raise NotImplementedError(
                "ChronicleClient is not available in this environment.")


class SecOpsClient:
    """Main client class for interacting with Google SecOps."""

    def __init__(
        self,
        credentials: Optional[_ga_credentials.Credentials] = None,
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
            # Try to use default credentials from environment
            self._credentials, _ = _ga_credentials.default()

        # If impersonation requested, wrap credentials
        if impersonate_service_account:
            if not isinstance(self._credentials, _ga_credentials.Credentials):
                raise TypeError(
                    "Base credentials must be a google.auth.credentials.Credentials instance"
                )
            # Default scopes for SecOps APIs
            scopes = ["https://www.googleapis.com/auth/cloud-platform"]
            self._credentials = ImpersonatedCredentials(
                source_credentials=self._credentials,
                target_principal=impersonate_service_account,
                target_scopes=scopes,
                lifetime=3600,
            )

        # Validate that we have credentials
        if not isinstance(self._credentials, _ga_credentials.Credentials):
            raise ValueError("Unable to obtain valid Google credentials")

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
            credentials=self._credentials,
            customer_id=customer_id,
            project_id=project_id,
            region=region,
        )
