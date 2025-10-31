from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any as ChronicleClient  # type: ignore[no-redef]


class SecOpsClient:
    def __init__(
        self,
        credentials: Optional["Credentials"] = None,
        service_account_path: Optional[str] = None,
        service_account_info: Optional[Dict[str, Any]] = None,
        impersonate_service_account: Optional[str] = None,
    ):
        self._credentials = None

        if credentials is not None:
            self._credentials = credentials
        else:
            try:
                # Defer heavy imports to runtime
                from google.oauth2 import service_account as gsa
                import google.auth

                if service_account_path:
                    self._credentials = gsa.Credentials.from_service_account_file(
                        service_account_path,
                        scopes=["https://www.googleapis.com/auth/cloud-platform"],
                    )
                elif service_account_info:
                    self._credentials = gsa.Credentials.from_service_account_info(
                        service_account_info,
                        scopes=["https://www.googleapis.com/auth/cloud-platform"],
                    )
                else:
                    self._credentials, _ = google.auth.default(
                        scopes=["https://www.googleapis.com/auth/cloud-platform"]
                    )
            except ImportError:
                if service_account_path or service_account_info:
                    raise ImportError(
                        "google-auth is required to load service account credentials."
                    )
                # If user didn't supply credentials and google-auth is missing
                # we leave credentials as None; downstream clients may support that.
                self._credentials = None

        if impersonate_service_account:
            try:
                from google.auth import impersonated_credentials
                from google.auth.transport.requests import Request
                import google.auth

                source_credentials = self._credentials
                if source_credentials is None:
                    source_credentials, _ = google.auth.default(
                        scopes=["https://www.googleapis.com/auth/cloud-platform"]
                    )

                if source_credentials and hasattr(source_credentials, "with_scopes"):
                    source_credentials = source_credentials.with_scopes(
                        ["https://www.googleapis.com/auth/cloud-platform"]
                    )

                # Refresh source to ensure it has an access token for impersonation
                if hasattr(source_credentials, "refresh"):
                    source_credentials.refresh(Request())

                self._credentials = impersonated_credentials.Credentials(
                    source_credentials=source_credentials,
                    target_principal=impersonate_service_account,
                    target_scopes=[
                        "https://www.googleapis.com/auth/cloud-platform"],
                    lifetime=3600,
                )
            except ImportError:
                raise ImportError(
                    "google-auth is required to impersonate a service account."
                )

    def chronicle(self, customer_id: str, project_id: str, region: str = "us") -> "ChronicleClient":
        client_cls = None
        err: Optional[Exception] = None

        for path in (
            # Prefer relative import assuming package structure
            ".chronicle",
            "chronicle",
            "secops.chronicle",
        ):
            try:
                if path.startswith("."):
                    # Relative import; determine package dynamically
                    from importlib import import_module

                    module = import_module(path, package=__package__)
                else:
                    from importlib import import_module

                    module = import_module(path)

                client_cls = getattr(module, "ChronicleClient")
                break
            except Exception as e:
                err = e
                continue

        if client_cls is None:
            raise ImportError(
                f"Could not import ChronicleClient. Last error: {err!r}"
            )

        return client_cls(
            credentials=self._credentials,
            customer_id=customer_id,
            project_id=project_id,
            region=region,
        )
