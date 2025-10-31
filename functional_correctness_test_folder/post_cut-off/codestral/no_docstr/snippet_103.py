
import numpy as np
from typing import List
import requests


class TritonRemoteModel:

    def __init__(self, url: str, endpoint: str = '', scheme: str = ''):
        self.url = url
        self.endpoint = endpoint
        self.scheme = scheme

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        data = {
            'inputs': [input_.tolist() for input_ in inputs]
        }
        response = requests.post(
            f"{self.scheme}://{self.url}/{self.endpoint}", json=data)
        response.raise_for_status()
        outputs = response.json()['outputs']
        return [np.array(output) for output in outputs]
