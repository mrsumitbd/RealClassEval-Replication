
class UnifiedAuthFactory:

    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> 'ModelAuthProvider':
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
            raise ValueError(
                f"Provider {provider} is not supported for model authentication.")

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> 'StorageAuthProvider':
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
            raise ValueError(
                f"Provider {provider} is not supported for storage authentication.")


class ModelAuthProvider:
    def __init__(self, **kwargs):
        pass


class StorageAuthProvider:
    def __init__(self, **kwargs):
        pass


class OCIModelAuthProvider(ModelAuthProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AWSModelAuthProvider(ModelAuthProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AzureModelAuthProvider(ModelAuthProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GCPModelAuthProvider(ModelAuthProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GitHubModelAuthProvider(ModelAuthProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class OCIStorageAuthProvider(StorageAuthProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AWSStorageAuthProvider(StorageAuthProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class AzureStorageAuthProvider(StorageAuthProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GCPStorageAuthProvider(StorageAuthProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GitHubStorageAuthProvider(StorageAuthProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
