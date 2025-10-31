import random
from typing import List, Dict, Optional, Any, Union
from typing import Optional, Dict, Any, List
from datetime import datetime
from datetime import datetime

class MockLiteLLMResponse:
    """
    Mock class for testing LiteLLM completion responses.
    Simulates both standard text completions and function calling responses.
    """

    def __init__(self, model: str='gpt-3.5-turbo', messages: List[Dict[str, str]]=None, functions: Optional[List[Dict[str, Any]]]=None, mock_responses: List[str]=None):
        self.model = model
        self.messages = messages or []
        self.functions = functions
        self.mock_responses = mock_responses or ['This is a mock response.', "Here's another possible response.", 'And one more mock response option.']
        self._generate_response_id()

    def _generate_response_id(self) -> None:
        """Generate a unique response ID similar to OpenAI's format."""
        timestamp = datetime.now().strftime('%Y%m%d')
        self.response_id = f'mock-{timestamp}-{random.randint(1000, 9999)}'

    def _create_base_response(self) -> Dict[str, Any]:
        """Create the base response structure."""
        return {'id': self.response_id, 'object': 'chat.completion', 'created': int(datetime.now().timestamp()), 'model': self.model, 'usage': {'prompt_tokens': random.randint(50, 200), 'completion_tokens': random.randint(20, 100), 'total_tokens': random.randint(70, 300)}}

    def _create_function_call_response(self) -> Dict[str, Any]:
        """Create a response that includes a function call."""
        if not self.functions:
            raise ValueError('No functions provided for function call response')
        selected_function = random.choice(self.functions)
        function_name = selected_function['name']
        mock_params = {}
        if 'parameters' in selected_function:
            for param_name, param_info in selected_function['parameters'].get('properties', {}).items():
                if param_info.get('type') == 'string':
                    mock_params[param_name] = f'mock_{param_name}'
                elif param_info.get('type') == 'number':
                    mock_params[param_name] = random.randint(1, 100)
                elif param_info.get('type') == 'boolean':
                    mock_params[param_name] = random.choice([True, False])
        response = self._create_base_response()
        response['choices'] = [{'index': 0, 'message': {'role': 'assistant', 'content': None, 'function_call': {'name': function_name, 'arguments': str(mock_params)}}, 'finish_reason': 'function_call'}]
        return response

    def _create_text_response(self) -> Dict[str, Any]:
        """Create a standard text completion response."""
        response = self._create_base_response()
        response['choices'] = [{'index': 0, 'message': {'role': 'assistant', 'content': random.choice(self.mock_responses)}, 'finish_reason': 'stop'}]
        return response

    def get_response(self) -> Dict[str, Any]:
        """
        Get a mock completion response.
        Randomly decides between function call and text response if functions are available.
        """
        if self.functions and random.random() < 0.5:
            return self._create_function_call_response()
        return self._create_text_response()