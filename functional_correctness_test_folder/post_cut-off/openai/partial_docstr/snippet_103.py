
import numpy as np
from typing import List, Optional
import tritonclient.http as httpclient
import tritonclient.grpc as grpcclient
from tritonclient.utils import np_dtype_from_triton_dtype


class TritonRemoteModel:
    '''
    Client for interacting with a remote Triton Inference Server model.
    Attributes:
        endpoint (str): The name of the model on the Triton server.
        url (str): The URL of the Triton server.
        triton_client: The Triton client (either HTTP or gRPC).
        InferInput: The input class for the Triton client.
        InferRequestedOutput: The output request class for the Triton client.
        input_formats (List[str]): The data types of the model inputs.
        np_input_formats (List[type]): The numpy data types of the model inputs.
        input_names (List[str]): The names of the model inputs.
        output_names (List[str]): The names of the model outputs.
    '''

    def __init__(self, url: str, endpoint: str = '', scheme: str = ''):
        # Determine scheme if not provided
        if not scheme:
            if url.startswith('http://') or url.startswith('https://'):
                scheme = 'http'
            elif url.startswith('grpc://'):
                scheme = 'grpc'
            else:
                scheme = 'http'  # default to HTTP

        # Strip scheme prefix from URL for client initialization
        if scheme == 'http':
            if url.startswith('http://'):
                host = url[len('http://'):]
            elif url.startswith('https://'):
                host = url[len('https://'):]
            else:
                host = url
            self.triton_client = httpclient.InferenceServerClient(
                url=host, verbose=False)
            self.InferInput = httpclient.InferInput
            self.InferRequestedOutput = httpclient.InferRequestedOutput
        else:  # grpc
            if url.startswith('grpc://'):
                host = url[len('grpc://'):]
            else:
                host = url
            self.triton_client = grpcclient.InferenceServerClient(
                url=host, verbose=False)
            self.InferInput = grpcclient.InferInput
            self.InferRequestedOutput = grpcclient.InferRequestedOutput

        self.url = url
        self.endpoint = endpoint

        # Retrieve model metadata
        metadata = self.triton_client.get_model_metadata(self.endpoint)
        self.input_names = [inp['name'] for inp in metadata['inputs']]
        self.output_names = [out['name'] for out in metadata['outputs']]

        # Input formats
        self.input_formats = [inp['datatype'] for inp in metadata['inputs']]
        self.np_input_formats = [np_dtype_from_triton_dtype(
            dt) for dt in self.input_formats]

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        if len(inputs) != len(self.input_names):
            raise ValueError(
                f'Expected {len(self.input_names)} inputs, got {len(inputs)}'
            )

        # Prepare InferInput objects
        triton_inputs = []
        for name, inp, dtype, shape in zip(
            self.input_names, inputs, self.input_formats, [
                i.shape for i in inputs]
        ):
            triton_inp = self.InferInput(name, shape, dtype)
            triton_inp.set_data_from_numpy(inp)
            triton_inputs.append(triton_inp)

        # Prepare InferRequestedOutput objects
        triton_outputs = [
            self.InferRequestedOutput(name) for name in self.output_names
        ]

        # Perform inference
        response = self.triton_client.infer(
            model_name=self.endpoint,
            inputs=triton_inputs,
            outputs=triton_outputs,
        )

        # Extract outputs as numpy arrays
        outputs = []
        for name in self.output_names:
            outputs.append(response.as_numpy(name))
        return outputs
