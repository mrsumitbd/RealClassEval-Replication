
from typing import Dict, List


class ModelConfig:

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.model_info = self._get_model_info(model_name)

    def _get_model_info(self, model_name: str) -> Dict[str, str]:
        model_info_dict = {
            'model1': {'param1': 'value1', 'param2': 'value2'},
            'model2': {'param1': 'value3', 'param2': 'value4'},
            'model3': {'param1': 'value5', 'param2': 'value6'},
        }
        return model_info_dict.get(model_name, {})

    @classmethod
    def get_supported_models(cls) -> List[str]:
        return ['model1', 'model2', 'model3']
