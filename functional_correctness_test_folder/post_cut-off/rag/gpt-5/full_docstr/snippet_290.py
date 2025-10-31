from __future__ import annotations

from typing import Any, Dict, Optional, TYPE_CHECKING
import importlib


class SecOpsClient:
    """Main client class for interacting with Google SecOps."""

    DEFAULT_SCOPES = (
        "https://www.googleapis.com/auth/cloud-platform",
    )

    def __init__(
        self,
        credentials: Optional["Credentials"] = None,
        service_account_path: Optional[str] = None,
        service_account_info: Optional[Dict[str, Any]] = None,
        impersonate_service_account: Optional[str] = None,
    ):
        """Initialize the SecOps client.
        Args:
            credentials: Optional pre-existing Google Auth credentials
            service_account_path: Optional path to service account JSON key file
            service_account_info: Optional service account JSON key data as dict
            impersonate_service_account: Optional service account to impersonate
        """
        if service_account_path and service_account_info:
            raise ValueError(
                "Provide either service_account_path or service_account_info, not both.")

        creds = credentials

        if creds is None:
            if service_account_path or service_account_info:
                try:
                    from google.oauth2 import service_account as sa  # type: ignore
                except Exception as e:
                    raise ImportError(
                        "google-auth is required for service account credentials") from e

                if service_account_path:
                    creds = sa.Credentials.from_service_account_file(
                        service_account_path, scopes=self.DEFAULT_SCOPES)
                else:
                    creds = sa.Credentials.from_service_account_info(
                        service_account_info, scopes=self.DEFAULT_SCOPES)  # type: ignore[arg-type]
            else:
                try:
                    from google.auth import default as google_auth_default  # type: ignore
                except Exception as e:
                    raise ImportError(
                        "google-auth is required to obtain default application credentials") from e

                # Try to request scoped ADC. If not supported (older versions), fall back to scoping manually.
                try:
                    creds, _ = google_auth_default(
                        scopes=self.DEFAULT_SCOPES)  # type: ignore
                except TypeError:
                    creds, _ = google_auth_default()  # type: ignore
                    if getattr(creds, "requires_scopes", False) and hasattr(creds, "with_scopes"):
                        creds = creds.with_scopes(self.DEFAULT_SCOPES)

        # Optionally impersonate a target service account using the base credentials
        if impersonate_service_account:
            try:
                from google.auth.impersonated_credentials import Credentials as ImpersonatedCredentials  # type: ignore
            except Exception as e:
                raise ImportError(
                    "google-auth is required for service account impersonation") from e

            # Ensure source credentials have broad enough scope to call IAM for impersonation.
            if getattr(creds, "requires_scopes", False) and hasattr(creds, "with_scopes"):
                creds = creds.with_scopes(self.DEFAULT_SCOPES)

            creds = ImpersonatedCredentials(
                source_credentials=creds,  # type: ignore[arg-type]
                target_principal=impersonate_service_account,
                target_scopes=self.DEFAULT_SCOPES,
                lifetime=3600,
            )

        self.credentials = creds
        self.impersonated_service_account = impersonate_service_account

    def chronicle(self, customer_id: str, project_id: str, region: str = "us") -> "ChronicleClient":
        """Get Chronicle API client.
        Args:
            customer_id: Chronicle customer ID
            project_id: GCP project ID
            region: Chronicle API region (default: "us")
        Returns:
            ChronicleClient instance
        """
        # Try to resolve ChronicleClient dynamically without hard-coding module path
        ChronicleClient = None  # type: ignore
        if "ChronicleClient" in globals():
            # type: ignore[assignment]
            ChronicleClient = globals()["ChronicleClient"]
        else:
            for module_name in ("chronicle", "secops.chronicle", "google_secops.chronicle"):
                try:
                    mod = importlib.import_module(module_name)
                    ChronicleClient = getattr(mod, "ChronicleClient", None)
                    if ChronicleClient:
                        break
                except Exception:
                    continue
        if ChronicleClient is None:
            raise ImportError(
                "Unable to locate ChronicleClient. Ensure the Chronicle client implementation is importable."
            )

        return ChronicleClient(  # type: ignore[call-arg]
            customer_id=customer_id,
            project_id=project_id,
            region=region,
            credentials=self.credentials,
        )
