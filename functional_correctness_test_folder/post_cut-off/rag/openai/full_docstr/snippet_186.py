
from __future__ import annotations

from typing import Any, Dict

# Import the base provider classes and concrete implementations.
# These imports assume the following module layout:
#   hdx.auth.model_auth.{OpenAIAuthProvider, OCIModelAuthProvider, AWSBedrockAuthProvider,
#                           AzureOpenAIAuthProvider, GCPVertexAuthProvider, ModelAuthProvider}
#   hdx.auth.storage_auth.{OCIStorageAuthProvider, AWSStorageAuthProvider,
#                           AzureStorageAuthProvider, GCPStorageAuthProvider,
#                           GitHubStorageAuthProvider, StorageAuthProvider}
# Adjust the import paths if the actual package structure differs.

try:
    from hdx.auth.model_auth import (
        OpenAIAuthProvider,
        OCIModelAuthProvider,
        AWSBedrockAuthProvider,
        AzureOpenAIAuthProvider,
        GCPVertexAuthProvider,
        ModelAuthProvider,
    )
except Exception:  # pragma: no cover
    # Fallback: define minimal stubs for type checking / documentation purposes.
    class ModelAuthProvider:  # type: ignore
        pass

    class OpenAIAuthProvider(ModelAuthProvider):  # type: ignore
        def __init__(self, **kwargs: Any) -> None:  # pragma: no cover
            pass

    class OCIModelAuthProvider(ModelAuthProvider):  # type: ignore
        def __init__(self, **kwargs: Any) -> None:  # pragma: no cover
            pass

    class AWSBedrockAuthProvider(ModelAuthProvider):  # type: ignore
        def __init__(self, **kwargs: Any) -> None:  # pragma: no cover
            pass

    class AzureOpenAIAuthProvider(ModelAuthProvider):  # type: ignore
        def __init__(self, **kwargs: Any) -> None:  # pragma: no cover
            pass

    class GCPVertexAuthProvider(ModelAuthProvider):  # type: ignore
        def __init__(self, **kwargs: Any) -> None:  # pragma: no cover
            pass

try:
    from hdx.auth.storage_auth import (
        OCIStorageAuthProvider,
        AWSStorageAuthProvider,
        AzureStorageAuthProvider,
        GCPStorageAuthProvider,
        GitHubStorageAuthProvider,
        StorageAuthProvider,
    )
except Exception:  # pragma: no cover
    # Fallback stubs
    class StorageAuthProvider:  # type: ignore
        pass

    class OCIStorageAuthProvider(StorageAuthProvider):  # type: ignore
        def __init__(self, **kwargs: Any) -> None:  # pragma: no cover
            pass

    class AWSStorageAuthProvider(StorageAuthProvider):  # type: ignore
        def __init__(self, **kwargs: Any) -> None:  # pragma: no cover
            pass

    class AzureStorageAuthProvider(StorageAuthProvider):  # type: ignore
        def __init__(self, **kwargs: Any) -> None:  # pragma: no cover
            pass

    class GCPStorageAuthProvider(StorageAuthProvider):  # type: ignore
        def __init__(self, **kwargs: Any) -> None:  # pragma: no cover
            pass

    class GitHubStorageAuthProvider(StorageAuthProvider):  # type: ignore
        def __init__(self, **kwargs: Any) -> None:  # pragma: no cover
            pass


class UnifiedAuthFactory:
    """Factory for creating model and storage authentication providers."""

    @staticmethod
    def create_model_auth(provider: str, **kwargs: Any) -> ModelAuthProvider:
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
        provider_map: Dict[str, type[ModelAuthProvider]] = {
            "openai": OpenAIAuthProvider,
            "oci": OCIModelAuthProvider,
            "aws-bedrock": AWSBedrockAuthProvider,
            "azure-openai": AzureOpenAIAuthProvider,
            "gcp-vertex": GCPVertexAuthProvider,
        }

        key = provider.lower()
        if key not in provider_map:
            raise ValueError(f"Unsupported model provider: {provider!r}")

        provider_cls = provider_map[key]
        return provider_cls(**kwargs)

    @staticmethod
    def create_storage_auth(provider: str, **kwargs: Any) -> StorageAuthProvider:
        """Create a storage authentication provider.

        Args:
            provider: Provider type ('oci', 'aws', 'azure', 'gcp', 'github')
            **kwargs: Provider-specific arguments

        Returns:
            StorageAuthProvider instance

        Raises:
            ValueError: If provider is not supported
        """
        provider_map: Dict[str, type[StorageAuthProvider]] = {
            "oci": OCIStorageAuthProvider,
            "aws": AWSStorageAuthProvider,
            "azure": AzureStorageAuthProvider,
            "gcp": GCPStorageAuthProvider,
            "github": GitHubStorageAuthProvider,
        }

        key = provider.lower()
        if key not in provider_map:
            raise ValueError(f"Unsupported storage provider: {provider!r}")

        provider_cls = provider_map[key]
        return provider_cls(**kwargs)
