from typing import Any, Tuple
from dataclasses import dataclass, field

@dataclass
class OasOperation:
    tags: list
    summary: str
    description: str
    operation_id: str
    request_schema: Any
    response_schema: Any
    path_parameters: dict
    query_parameters: dict

    def _parameters_to_openapi(self):
        for key, value in sorted(self.path_parameters.items()):
            yield {'name': key, 'in': 'path', 'required': True, 'schema': {'type': value}}
        for key, value in sorted(self.query_parameters.get('properties', {}).items()):
            yield {'name': key, 'in': 'query', 'required': key in self.query_parameters.get('required', {}), 'schema': value}

    def _to_dict(self):
        result = {'tags': self.tags, 'description': tidy_string(self.description) or 'None.', 'operationId': self.operation_id, 'parameters': list(self._parameters_to_openapi())}
        if self.summary:
            result['summary'] = self.summary
        if self.request_schema:
            result['requestBody'] = {'content': {'application/json': {'schema': self.request_schema}}}
        result['responses'] = {'200': {'description': self.summary or 'OK'}}
        if self.response_schema:
            result['responses']['200']['content'] = {'application/json': {'schema': self.response_schema}}
        return result