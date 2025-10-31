
from typing import Dict, List


class ModelConfig:

    _MODELS = {
        "resnet50": {"type": "CNN", "input_size": "224x224", "framework": "PyTorch"},
        "bert-base": {"type": "Transformer", "input_size": "512", "framework": "TensorFlow"},
        "mobilenetv2": {"type": "CNN", "input_size": "224x224", "framework": "TensorFlow"},
        "gpt-2": {"type": "Transformer", "input_size": "1024", "framework": "PyTorch"},
    }

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model_info = self._get_model_info(model_name)

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        if model_name not in self._MODELS:
            raise ValueError(f"Model '{model_name}' is not supported.")
        return self._MODELS[model_name].copy()

    @classmethod
    def get_supported_models(cls) -> List[str]:
        return list(cls._MODELS.keys())
