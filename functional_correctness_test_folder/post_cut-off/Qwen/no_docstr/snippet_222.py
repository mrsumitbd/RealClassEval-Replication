
from typing import Dict, List


class ModelConfig:

    _supported_models = {
        "model_a": {"description": "This is model A", "version": "1.0"},
        "model_b": {"description": "This is model B", "version": "2.0"},
        "model_c": {"description": "This is model C", "version": "3.0"}
    }

    def __init__(self, model_name: str):
        if model_name not in self._supported_models:
            raise ValueError(f"Model {model_name} is not supported.")
        self.model_name = model_name
        self.model_info = self._get_model_info(model_name)

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        return self._supported_models.get(model_name, {})

    @classmethod
    def get_supported_models(cls) -> List[str]:
        return list(cls._supported_models.keys())
