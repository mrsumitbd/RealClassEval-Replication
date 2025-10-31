
from typing import Any, Dict

# Import the base provider classes
try:
    from .model_auth import ModelAuthProvider
except Exception:
    # Fallback for environments where the relative import fails
    from model_auth import ModelAuthProvider

try:
    from .storage_auth import StorageAuthProvider
except Exception:
    from storage_auth import StorageAuthProvider

# Import concrete provider implementations
try:
    from .model_auth import (
        OpenAIAuthProvider,
        OCIAuthProvider,
        AWSBedrockAuthProvider,
        AzureOpenAIAuthProvider,
        GCPVertexAuthProvider,
    )
except Exception:
    # Fallback imports if the module structure differs
    from model_auth import (
        OpenAIAuthProvider,
        OCIAuthProvider,
        AWSBedrockAuthProvider,
        AzureOpenAIAuthProvider,
        GCPVertexAuthProvider,
    )

try:
    from .storage_auth import (
        OCIStorageAuthProvider,
        AWSStorageAuthProvider,
        AzureStorageAuthProvider,
        GCPStorageAuthProvider,
        GitHubStorageAuthProvider,
    )
except Exception:
    from storage_auth import (
        OCIStorageAuthProvider,
        AWSStorageAuthProvider,
        AzureStorageAuthProvider,
        GCPStorageAuthProvider,
        GitHubStorageAuthProvider,
    )


class UnifiedAuthFactory:
    """Factory for creating model and storage authentication providers."""

    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> ModelAuthProvider:
        """Create a model endpoint authentication provider.

        Args:
            provider: Provider type ('openai', 'oci', 'aws-bedrock',
                'azure-openai', 'gcp-vertex')
            **kwargs: Provider-specific arguments

        Returns:
            ModelAuthProvider instance

        Raises:
            ValueError: If provider is not supported
        """
        provider = provider.lower()
        mapping: Dict[str, Any] = {
            "openai": OpenAIAuthProvider,
            "oci": OCIAuthProvider,
            "aws-bedrock": AWSBedrockAuthProvider,
            "azure-openai": AzureOpenAIAuthProvider,
            "gcp-vertex": GCPVertexAuthProvider,
        }

        if provider not in mapping:
            raise ValueError(f"Unsupported model provider: {provider!r}")

        provider_cls = mapping[provider]
        return provider_cls(**kwargs)

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> StorageAuthProvider:
        """Create a storage authentication provider.

        Args:
            provider: Provider type ('oci', 'aws', 'azure', 'gcp', 'github')
            **kwargs: Provider-specific arguments

        Returns:
            StorageAuthProvider instance

        Raises:
            ValueError: If provider is not supported
        """
        provider = provider.lower()
        mapping: Dict[str, Any] = {
            "oci": OCIStorageAuthProvider,
            "aws": AWSStorageAuthProvider,
            "azure": AzureStorageAuthProvider,
            "gcp": GCPStorageAuthProvider,
            "github": GitHubStorageAuthProvider,
        }

        if provider not in mapping:
            raise ValueError(f"Unsupported storage provider: {provider!r}")

        provider_cls = mapping[provider]
        return provider_cls(**kwargs)
