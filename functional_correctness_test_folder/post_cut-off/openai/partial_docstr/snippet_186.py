
from typing import Type

# Import provider classes (adjust imports to match actual module structure)
try:
    from .oci_auth import OciModelAuthProvider, OciStorageAuthProvider
    from .aws_auth import AwsModelAuthProvider, AwsStorageAuthProvider
    from .azure_auth import AzureModelAuthProvider, AzureStorageAuthProvider
    from .gcp_auth import GcpModelAuthProvider, GcpStorageAuthProvider
    from .github_auth import GithubModelAuthProvider, GithubStorageAuthProvider
except Exception:
    # Fallback: define minimal stubs if imports fail (for environments without the full package)
    class OciModelAuthProvider:
        pass

    class OciStorageAuthProvider:
        pass

    class AwsModelAuthProvider:
        pass

    class AwsStorageAuthProvider:
        pass

    class AzureModelAuthProvider:
        pass

    class AzureStorageAuthProvider:
        pass

    class GcpModelAuthProvider:
        pass

    class GcpStorageAuthProvider:
        pass

    class GithubModelAuthProvider:
        pass

    class GithubStorageAuthProvider:
        pass


class UnifiedAuthFactory:
    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> 'ModelAuthProvider':
        provider_map: dict[str, Type] = {
            'oci': OciModelAuthProvider,
            'aws': AwsModelAuthProvider,
            'azure': AzureModelAuthProvider,
            'gcp': GcpModelAuthProvider,
            'github': GithubModelAuthProvider,
        }
        provider_cls = provider_map.get(provider.lower())
        if provider_cls is None:
            raise ValueError(f"Unsupported model auth provider: {provider}")
        return provider_cls(**kwargs)

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> 'StorageAuthProvider':
        '''Create a storage authentication provider.
        Args:
            provider: Provider type ('oci', 'aws', 'azure', 'gcp', 'github')
            **kwargs: Provider-specific arguments
        Returns:
            StorageAuthProvider instance
        Raises:
            ValueError: If provider is not supported
        '''
        provider_map: dict[str, Type] = {
            'oci': OciStorageAuthProvider,
            'aws': AwsStorageAuthProvider,
            'azure': AzureStorageAuthProvider,
            'gcp': GcpStorageAuthProvider,
            'github': GithubStorageAuthProvider,
        }
        provider_cls = provider_map.get(provider.lower())
        if provider_cls is None:
            raise ValueError(f"Unsupported storage auth provider: {provider}")
        return provider_cls(**kwargs)
