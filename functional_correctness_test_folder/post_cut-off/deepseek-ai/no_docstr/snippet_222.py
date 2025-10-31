
from typing import Dict, List


class ModelConfig:

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model_info = self._get_model_info(model_name)

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        supported_models = self.get_supported_models()
        if model_name not in supported_models:
            raise ValueError(f"Model {model_name} is not supported.")
        return {
            "name": model_name,
            "description": f"Configuration for {model_name} model"
        }

    @classmethod
    def get_supported_models(cls) -> List[str]:
        return ["resnet50", "bert-base", "gpt2", "vgg16"]
