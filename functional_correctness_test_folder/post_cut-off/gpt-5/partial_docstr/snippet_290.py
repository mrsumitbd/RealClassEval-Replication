from typing import Optional, Dict, Any, TYPE_CHECKING

try:
    from google.auth import default as google_auth_default
    from google.auth.credentials import Credentials as GoogleAuthCredentials
    from google.auth.impersonated_credentials import Credentials as ImpersonatedCredentials
    from google.oauth2.service_account import Credentials as ServiceAccountCredentials
except Exception:  # pragma: no cover
    google_auth_default = None
    GoogleAuthCredentials = None
    ImpersonatedCredentials = None
    ServiceAccountCredentials = None

if TYPE_CHECKING:
    from typing import Type
    ChronicleClient = object
else:
    ChronicleClient = object  # runtime placeholder


class SecOpsClient:
    DEFAULT_SCOPES = ("https://www.googleapis.com/auth/cloud-platform",)

    def __init__(
        self,
        credentials: Optional["GoogleAuthCredentials"] = None,
        service_account_path: Optional[str] = None,
        service_account_info: Optional[Dict[str, Any]] = None,
        impersonate_service_account: Optional[str] = None,
    ):
        if sum(
            1
            for x in (credentials, service_account_path, service_account_info)
            if x is not None
        ) > 1:
            raise ValueError(
                "Provide only one of: credentials, service_account_path, service_account_info"
            )

        if google_auth_default is None:
            raise ImportError(
                "google-auth is required. Install with: pip install google-auth"
            )

        base_credentials: Optional[GoogleAuthCredentials] = None

        if credentials is not None:
            base_credentials = credentials
        elif service_account_path is not None:
            if ServiceAccountCredentials is None:
                raise ImportError(
                    "google-auth is required. Install with: pip install google-auth"
                )
            base_credentials = ServiceAccountCredentials.from_service_account_file(
                service_account_path, scopes=self.DEFAULT_SCOPES
            )
        elif service_account_info is not None:
            if ServiceAccountCredentials is None:
                raise ImportError(
                    "google-auth is required. Install with: pip install google-auth"
                )
            base_credentials = ServiceAccountCredentials.from_service_account_info(
                service_account_info, scopes=self.DEFAULT_SCOPES
            )
        else:
            base_credentials, _ = google_auth_default(
                scopes=list(self.DEFAULT_SCOPES))

        if impersonate_service_account:
            if ImpersonatedCredentials is None:
                raise ImportError(
                    "google-auth is required. Install with: pip install google-auth"
                )
            base_credentials = ImpersonatedCredentials(
                source_credentials=base_credentials,
                target_principal=impersonate_service_account,
                target_scopes=list(self.DEFAULT_SCOPES),
                lifetime=3600,
            )

        self._credentials = base_credentials

    def chronicle(self, customer_id: str, project_id: str, region: str = "us"):
        try:
            # Attempt common relative import first
            from .chronicle import ChronicleClient as _ChronicleClient  # type: ignore
        except Exception:
            try:
                # Fallback absolute import path if packaged differently
                from chronicle import ChronicleClient as _ChronicleClient  # type: ignore
            except Exception as exc:
                raise ImportError(
                    "Unable to import ChronicleClient. Ensure the Chronicle client module is available."
                ) from exc

        return _ChronicleClient(
            customer_id=customer_id,
            project_id=project_id,
            region=region,
            credentials=self._credentials,
        )
