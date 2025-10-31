
import numpy as np
from typing import List
import requests


class TritonRemoteModel:

    def __init__(self, url: str, endpoint: str = '', scheme: str = 'http'):
        self.url = f"{scheme}://{url}"
        self.endpoint = endpoint

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        # Assuming the model expects inputs in a specific format, e.g., a JSON payload
        # Convert numpy arrays to lists for JSON serialization
        payload = {'inputs': [{'data': input.tolist()} for input in inputs]}

        response = requests.post(f"{self.url}/{self.endpoint}", json=payload)
        response.raise_for_status()  # Raise an error for bad responses

        # Assuming the response is in JSON format and contains a list of outputs
        result = response.json()
        outputs = [np.array(output['data']) for output in result['outputs']]

        return outputs
