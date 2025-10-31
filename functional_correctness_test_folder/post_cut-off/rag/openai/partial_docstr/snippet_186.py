
from typing import Any, Dict

# Import the base provider classes and concrete implementations.
# The exact import paths may vary depending on the project structure.
# Adjust the imports below to match your codebase.

try:
    # Base provider interfaces
    from hdx.hdx_api.auth import ModelAuthProvider, StorageAuthProvider

    # Model authentication providers
    from hdx.hdx_api.auth import (
        OpenAIAuthProvider,
        OCIAuthProvider,
        AWSBedrockAuthProvider,
        AzureOpenAIAuthProvider,
        GCPVertexAuthProvider,
    )

    # Storage authentication providers
    from hdx.hdx_api.auth import (
        OCIStorageAuthProvider,
        AWSStorageAuthProvider,
        AzureStorageAuthProvider,
        GCPStorageAuthProvider,
        GitHubStorageAuthProvider,
    )
except Exception:
    # Fallback imports if the above paths are incorrect.
    # Replace these with the correct module paths in your project.
    from hdx.hdx_api.auth import (
        ModelAuthProvider,
        StorageAuthProvider,
        OpenAIAuthProvider,
        OCIAuthProvider,
        AWSBedrockAuthProvider,
        AzureOpenAIAuthProvider,
        GCPVertexAuthProvider,
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
        if provider == "openai":
            return OpenAIAuthProvider(**kwargs)
        if provider == "oci":
            return OCIAuthProvider(**kwargs)
        if provider == "aws-bedrock":
            return AWSBedrockAuthProvider(**kwargs)
        if provider == "azure-openai":
            return AzureOpenAIAuthProvider(**kwargs)
        if provider == "gcp-vertex":
            return GCPVertexAuthProvider(**kwargs)

        raise ValueError(f"Unsupported model provider: {provider}")

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
        if provider == "oci":
            return OCIStorageAuthProvider(**kwargs)
        if provider == "aws":
            return AWSStorageAuthProvider(**kwargs)
        if provider == "azure":
            return AzureStorageAuthProvider(**kwargs)
        if provider == "gcp":
            return GCPStorageAuthProvider(**kwargs)
        if provider == "github":
            return GitHubStorageAuthProvider(**kwargs)

        raise ValueError(f"Unsupported storage provider: {provider}")
