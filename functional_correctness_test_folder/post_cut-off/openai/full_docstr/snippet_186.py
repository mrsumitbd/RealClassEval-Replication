
class ModelAuthProvider:
    """Base class for model authentication providers."""

    def __init__(self, **kwargs):
        self.params = kwargs


class StorageAuthProvider:
    """Base class for storage authentication providers."""

    def __init__(self, **kwargs):
        self.params = kwargs


# Model provider implementations
class OpenAIAuthProvider(ModelAuthProvider):
    pass


class OCIAuthProvider(ModelAuthProvider):
    pass


class AWSBedrockAuthProvider(ModelAuthProvider):
    pass


class AzureOpenAIAuthProvider(ModelAuthProvider):
    pass


class GCPVertexAuthProvider(ModelAuthProvider):
    pass


# Storage provider implementations
class OCIStorageAuthProvider(StorageAuthProvider):
    pass


class AWSStorageAuthProvider(StorageAuthProvider):
    pass


class AzureStorageAuthProvider(StorageAuthProvider):
    pass


class GCPStorageAuthProvider(StorageAuthProvider):
    pass


class GitHubStorageAuthProvider(StorageAuthProvider):
    pass


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
        provider_map = {
            "openai": OpenAIAuthProvider,
            "oci": OCIAuthProvider,
            "aws-bedrock": AWSBedrockAuthProvider,
            "azure-openai": AzureOpenAIAuthProvider,
            "gcp-vertex": GCPVertexAuthProvider,
        }

        key = provider.lower()
        if key not in provider_map:
            raise ValueError(f"Unsupported model provider: {provider}")

        return provider_map[key](**kwargs)

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
        provider_map = {
            "oci": OCIStorageAuthProvider,
            "aws": AWSStorageAuthProvider,
            "azure": AzureStorageAuthProvider,
            "gcp": GCPStorageAuthProvider,
            "github": GitHubStorageAuthProvider,
        }

        key = provider.lower()
        if key not in provider_map:
            raise ValueError(f"Unsupported storage provider: {provider}")

        return provider_map[key](**kwargs)
