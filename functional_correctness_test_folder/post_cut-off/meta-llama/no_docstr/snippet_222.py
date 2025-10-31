
from typing import Dict, List


class ModelConfig:

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model_info = self._get_model_info(model_name)

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        # For demonstration purposes, assume we have a dictionary that maps model names to their info
        model_info_dict = {
            "model1": {"description": "Model 1", "version": "1.0"},
            "model2": {"description": "Model 2", "version": "2.0"},
        }
        if model_name not in model_info_dict:
            raise ValueError(f"Model '{model_name}' is not supported")
        return model_info_dict[model_name]

    @classmethod
    def get_supported_models(cls) -> List[str]:
        # For demonstration purposes, assume we have a list of supported model names
        return ["model1", "model2"]
