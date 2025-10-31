
from typing import Type

# Import the base provider interfaces
from .auth_base import ModelAuthProvider, StorageAuthProvider

# Import concrete provider implementations
from .model_auth_providers import (
    AwsModelAuthProvider,
    GcpModelAuthProvider,
    AzureModelAuthProvider,
    LocalModelAuthProvider,
)
from .storage_auth_providers import (
    AwsStorageAuthProvider,
    GcpStorageAuthProvider,
    AzureStorageAuthProvider,
    LocalStorageAuthProvider,
)


class UnifiedAuthFactory:
    """
    Factory for creating authentication provider instances for models and storage.
    """

    # Mapping of provider names to concrete classes
    _MODEL_AUTH_MAP: dict[str, Type[ModelAuthProvider]] = {
        "aws": AwsModelAuthProvider,
        "gcp": GcpModelAuthProvider,
        "azure": AzureModelAuthProvider,
        "local": LocalModelAuthProvider,
    }

    _STORAGE_AUTH_MAP: dict[str, Type[StorageAuthProvider]] = {
        "aws": AwsStorageAuthProvider,
        "gcp": GcpStorageAuthProvider,
        "azure": AzureStorageAuthProvider,
        "local": LocalStorageAuthProvider,
    }

    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> ModelAuthProvider:
        """
        Create an instance of a model authentication provider.

        Args:
            provider: The name of the provider (e.g., 'aws', 'gcp', 'azure', 'local').
            **kwargs: Additional keyword arguments to pass to the provider constructor.

        Returns:
            An instance of a subclass of ModelAuthProvider.

        Raises:
            ValueError: If the provider name is not supported.
        """
        provider_cls = UnifiedAuthFactory._MODEL_AUTH_MAP.get(provider.lower())
        if provider_cls is None:
            raise ValueError(f"Unsupported model auth provider: {provider}")
        return provider_cls(**kwargs)

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> StorageAuthProvider:
        """
        Create an instance of a storage authentication provider.

        Args:
            provider: The name of the provider (e.g., 'aws', 'gcp', 'azure', 'local').
            **kwargs: Additional keyword arguments to pass to the provider constructor.

        Returns:
            An instance of a subclass of StorageAuthProvider.

        Raises:
            ValueError: If the provider name is not supported.
        """
        provider_cls = UnifiedAuthFactory._STORAGE_AUTH_MAP.get(
            provider.lower())
        if provider_cls is None:
            raise ValueError(f"Unsupported storage auth provider: {provider}")
        return provider_cls(**kwargs)
