
class ModelAuthProvider:
    def __init__(self, provider: str, **kwargs):
        self.provider = provider
        self.kwargs = kwargs


class StorageAuthProvider:
    def __init__(self, provider: str, **kwargs):
        self.provider = provider
        self.kwargs = kwargs


class UnifiedAuthFactory:

    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> ModelAuthProvider:
        return ModelAuthProvider(provider, **kwargs)

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> StorageAuthProvider:
        return StorageAuthProvider(provider, **kwargs)
