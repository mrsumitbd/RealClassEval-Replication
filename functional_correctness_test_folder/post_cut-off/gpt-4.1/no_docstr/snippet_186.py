
class ModelAuthProvider:
    def __init__(self, **kwargs):
        self.config = kwargs


class StorageAuthProvider:
    def __init__(self, **kwargs):
        self.config = kwargs


class OpenAIModelAuth(ModelAuthProvider):
    pass


class HuggingFaceModelAuth(ModelAuthProvider):
    pass


class S3StorageAuth(StorageAuthProvider):
    pass


class GCSStorageAuth(StorageAuthProvider):
    pass


class UnifiedAuthFactory:

    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> ModelAuthProvider:
        provider = provider.lower()
        if provider == "openai":
            return OpenAIModelAuth(**kwargs)
        elif provider == "huggingface":
            return HuggingFaceModelAuth(**kwargs)
        else:
            raise ValueError(f"Unknown model auth provider: {provider}")

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> StorageAuthProvider:
        provider = provider.lower()
        if provider == "s3":
            return S3StorageAuth(**kwargs)
        elif provider == "gcs":
            return GCSStorageAuth(**kwargs)
        else:
            raise ValueError(f"Unknown storage auth provider: {provider}")
