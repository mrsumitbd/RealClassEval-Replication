
import numpy as np
import requests
from typing import List


class TritonRemoteModel:

    def __init__(self, url: str, endpoint: str = '', scheme: str = ''):
        self.url = url
        self.endpoint = endpoint
        self.scheme = scheme or 'http'

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        import tritonclient.http as httpclient
        from tritonclient.utils import np_to_triton_dtype

        client = httpclient.InferenceServerClient(url=self.url)

        input_tensors = []
        for idx, inp in enumerate(inputs):
            input_tensors.append(
                httpclient.InferInput(
                    f"INPUT_{idx}", inp.shape, np_to_triton_dtype(inp.dtype))
            )
            input_tensors[-1].set_data_from_numpy(inp)

        response = client.infer(model_name=self.endpoint, inputs=input_tensors)

        outputs = []
        for output in response.get_response()['outputs']:
            outputs.append(response.as_numpy(output['name']))

        return outputs
