
import numpy as np
import requests
from typing import List


class TritonRemoteModel:

    def __init__(self, url: str, endpoint: str = '', scheme: str = ''):
        self.url = url.rstrip('/')
        self.endpoint = endpoint
        self.scheme = scheme if scheme else 'http'
        if self.endpoint:
            self.full_url = f"{self.scheme}://{self.url}/{self.endpoint.lstrip('/')}"
        else:
            self.full_url = f"{self.scheme}://{self.url}"

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        data = []
        for arr in inputs:
            data.append({
                'shape': arr.shape,
                'dtype': str(arr.dtype),
                'data': arr.tolist()
            })
        payload = {'inputs': data}
        response = requests.post(self.full_url, json=payload)
        response.raise_for_status()
        result = response.json()
        outputs = []
        for out in result.get('outputs', []):
            arr = np.array(out['data'], dtype=out['dtype'])
            arr = arr.reshape(out['shape'])
            outputs.append(arr)
        return outputs
