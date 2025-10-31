
import numpy as np
from typing import List
import requests
import json


class TritonRemoteModel:

    def __init__(self, url: str, endpoint: str = '', scheme: str = 'http'):
        """
        Initialize the TritonRemoteModel class.

        Args:
        url (str): The URL of the Triton server.
        endpoint (str): The endpoint of the model. Defaults to ''.
        scheme (str): The scheme of the URL. Defaults to 'http'.
        """
        self.url = f"{scheme}://{url}{endpoint}" if not url.startswith(
            'http') else url + endpoint
        self.headers = {'Content-Type': 'application/json'}

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        """
        Make a prediction using the Triton model.

        Args:
        *inputs (np.ndarray): The input data.

        Returns:
        List[np.ndarray]: The output of the model.
        """
        # Create the request data
        data = {
            'inputs': [{'name': f'INPUT{i}', 'shape': input_.shape, 'datatype': 'FP32', 'data': input_.tolist()} for i, input_ in enumerate(inputs)],
            'outputs': [{'name': f'OUTPUT{i}'} for i in range(len(inputs))]
        }

        # Make the request
        response = requests.post(
            self.url, headers=self.headers, data=json.dumps(data))

        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(
                f"Failed to make prediction. Status code: {response.status_code}")

        # Parse the response
        response_data = json.loads(response.text)
        outputs = [np.array(output['data']).reshape(tuple(output['shape']))
                   for output in response_data['outputs']]

        return outputs
