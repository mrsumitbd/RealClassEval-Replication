
class UnifiedAuthFactory:

    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> ModelAuthProvider:
        if provider == 'aws':
            return AWSModelAuthProvider(**kwargs)
        elif provider == 'azure':
            return AzureModelAuthProvider(**kwargs)
        elif provider == 'gcp':
            return GCPModelAuthProvider(**kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> StorageAuthProvider:
        if provider == 'aws':
            return AWSStorageAuthProvider(**kwargs)
        elif provider == 'azure':
            return AzureStorageAuthProvider(**kwargs)
        elif provider == 'gcp':
            return GCPStorageAuthProvider(**kwargs)
        else:
            raise ValueError(f"Unsupported provider: {provider}")
