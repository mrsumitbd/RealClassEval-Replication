from typing import Any
from pydantic import BaseModel
from elysia.util.parsing import format_dict_to_serialisable
from copy import deepcopy

class TrainingUpdate:
    """
    Record a training example for a module.
    Keep track of the inputs and outputs of the module, and the module name.
    """

    def __init__(self, module_name: str, inputs: dict, outputs: dict, extra_inputs: dict={}):
        self.module_name = module_name
        format_dict_to_serialisable(inputs)
        format_dict_to_serialisable(outputs)
        inputs_copy = deepcopy(inputs)
        outputs_copy = deepcopy(outputs)
        for key, value in inputs_copy.items():
            inputs_copy[key] = self._convert_basemodel(value)
        for key, value in outputs_copy.items():
            outputs_copy[key] = self._convert_basemodel(value)
        self.inputs = {**inputs_copy, **extra_inputs}
        self.outputs = outputs_copy

    def _convert_basemodel(self, value: Any):
        if isinstance(value, BaseModel):
            return value.model_dump()
        elif isinstance(value, dict):
            return {k: self._convert_basemodel(v) for k, v in value.items()}
        elif isinstance(value, list):
            return [self._convert_basemodel(v) for v in value]
        else:
            return value

    def to_json(self):
        return {'module_name': self.module_name, 'inputs': self.inputs, 'outputs': self.outputs}