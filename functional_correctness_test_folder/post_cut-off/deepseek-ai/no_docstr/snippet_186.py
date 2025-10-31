
class UnifiedAuthFactory:

    @staticmethod
    def create_model_auth(provider: str, **kwargs) -> ModelAuthProvider:
        if provider == "openai":
            return OpenAIAuthProvider(**kwargs)
        elif provider == "huggingface":
            return HuggingFaceAuthProvider(**kwargs)
        elif provider == "anthropic":
            return AnthropicAuthProvider(**kwargs)
        else:
            raise ValueError(f"Unsupported model auth provider: {provider}")

    @staticmethod
    def create_storage_auth(provider: str, **kwargs) -> StorageAuthProvider:
        if provider == "aws":
            return AWSAuthProvider(**kwargs)
        elif provider == "gcp":
            return GCPAuthProvider(**kwargs)
        elif provider == "azure":
            return AzureAuthProvider(**kwargs)
        else:
            raise ValueError(f"Unsupported storage auth provider: {provider}")
