
class UnifiedAuthFactory:

    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> ModelAuthProvider:
        if provider == 'oci':
            return OCIModelAuthProvider(**kwargs)
        elif provider == 'aws':
            return AWSModelAuthProvider(**kwargs)
        elif provider == 'azure':
            return AzureModelAuthProvider(**kwargs)
        elif provider == 'gcp':
            return GCPModelAuthProvider(**kwargs)
        elif provider == 'github':
            return GitHubModelAuthProvider(**kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

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
        if provider == 'oci':
            return OCIStorageAuthProvider(**kwargs)
        elif provider == 'aws':
            return AWSStorageAuthProvider(**kwargs)
        elif provider == 'azure':
            return AzureStorageAuthProvider(**kwargs)
        elif provider == 'gcp':
            return GCPStorageAuthProvider(**kwargs)
        elif provider == 'github':
            return GitHubStorageAuthProvider(**kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
