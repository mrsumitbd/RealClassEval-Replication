from typing import Any, Dict, Optional

# Ensure type names exist even if not imported from elsewhere
try:
    ModelAuthProvider
except NameError:  # type: ignore
    class ModelAuthProvider:  # type: ignore
        pass

try:
    StorageAuthProvider
except NameError:  # type: ignore
    class StorageAuthProvider:  # type: ignore
        pass


class _GenericAuthProvider(ModelAuthProvider, StorageAuthProvider):  # type: ignore
    def __init__(self, provider: str, credentials: Optional[Dict[str, Any]] = None) -> None:
        self.provider = provider
        self.credentials = credentials or {}

    def __repr__(self) -> str:
        cls = self.__class__.__name__
        return f"{cls}(provider={self.provider!r}, credentials={list(self.credentials.keys())!r})"


class UnifiedAuthFactory:
    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> ModelAuthProvider:
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("provider must be a non-empty string")

        normalized = provider.strip().lower()

        supported = {
            # Public model APIs
            "openai",
            "anthropic",
            "cohere",
            "huggingface",
            # Cloud model platforms
            "aws", "bedrock",
            "azure", "azure_openai",
            "gcp", "vertexai",
            "oci", "oci_genai",
            # Generic token/api-key based
            "generic",
        }

        if normalized not in supported:
            raise ValueError(
                f"Unsupported model provider '{provider}'. Supported: {sorted(supported)}"
            )

        # Minimal normalization/aliasing
        alias_map = {
            "bedrock": "aws",
            "azure_openai": "azure",
            "vertexai": "gcp",
            "oci_genai": "oci",
        }
        resolved = alias_map.get(normalized, normalized)

        # Whitelist typical credential keys; preserve all kwargs to be flexible
        # Common keys across providers:
        common_keys = {
            # generic tokens/keys
            "api_key", "access_token", "token", "bearer_token", "key",
            # endpoints/regions
            "endpoint", "base_url", "region",
            # oauth2/client credentials
            "client_id", "client_secret", "audience", "scope", "refresh_token",
            # aws
            "aws_access_key_id", "aws_secret_access_key", "aws_session_token", "profile",
            # azure
            "tenant_id", "subscription_id", "resource_group", "deployment", "model",
            # gcp
            "project", "location", "service_account_json", "service_account_file",
            # oci
            "tenancy_ocid", "user_ocid", "fingerprint", "private_key", "private_key_path", "pass_phrase",
            # huggingface
            "organization",
        }

        creds: Dict[str, Any] = {k: v for k,
                                 v in kwargs.items() if k in common_keys}
        # Keep unspecified keys too, to maintain forward compatibility
        for k, v in kwargs.items():
            if k not in creds:
                creds[k] = v

        return _GenericAuthProvider(resolved, creds)

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> StorageAuthProvider:
        '''Create a storage authentication provider.
        Args:
            provider: Provider type ('oci', 'aws', 'azure', 'gcp', 'github')
            **kwargs: Provider-specific arguments
        Returns:
            StorageAuthProvider instance
        Raises:
            ValueError: If provider is not supported
        '''
        if not isinstance(provider, str) or not provider.strip():
            raise ValueError("provider must be a non-empty string")

        normalized = provider.strip().lower()
        supported = {"oci", "aws", "azure", "gcp", "github"}

        if normalized not in supported:
            raise ValueError(
                f"Unsupported storage provider '{provider}'. Supported: {sorted(supported)}"
            )

        # Collect typical credential keys but keep all kwargs
        whitelist = {
            # AWS S3
            "aws_access_key_id", "aws_secret_access_key", "aws_session_token", "region", "profile",
            # Azure Blob/DataLake
            "account_name", "account_key", "sas_token", "connection_string", "tenant_id",
            "client_id", "client_secret",
            # GCP GCS
            "project", "service_account_json", "service_account_file", "access_token",
            # OCI Object Storage
            "tenancy_ocid", "user_ocid", "fingerprint", "private_key", "private_key_path", "pass_phrase", "namespace",
            # GitHub (e.g., releases/assets, packages)
            "token", "username", "repo", "owner",
            # Endpoints/overrides
            "endpoint", "base_url",
        }

        creds: Dict[str, Any] = {k: v for k,
                                 v in kwargs.items() if k in whitelist}
        for k, v in kwargs.items():
            if k not in creds:
                creds[k] = v

        return _GenericAuthProvider(normalized, creds)
