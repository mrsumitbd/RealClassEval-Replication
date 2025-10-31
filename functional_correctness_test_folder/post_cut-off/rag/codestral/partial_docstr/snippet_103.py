
import numpy as np
from typing import List, Optional, Union
from tritonclient.http import InferenceServerClient as HTTPClient, InferInput, InferRequestedOutput
from tritonclient.grpc import InferenceServerClient as GRPCClient


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
        '''
        Initialize the TritonRemoteModel.
        Arguments may be provided individually or parsed from a collective 'url' argument of the form
            <scheme>://<netloc>/<endpoint>/<task_name>
        Args:
            url (str): The URL of the Triton server.
            endpoint (str): The name of the model on the Triton server.
            scheme (str): The communication scheme ('http' or 'grpc').
        '''
        if not scheme and not endpoint:
            scheme, netloc, endpoint, _ = self._parse_url(url)
            url = f"{scheme}://{netloc}"
        elif not scheme:
            scheme = 'http'

        self.endpoint = endpoint
        self.url = url
        self.scheme = scheme.lower()

        if self.scheme == 'http':
            self.triton_client = HTTPClient(url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput
        elif self.scheme == 'grpc':
            self.triton_client = GRPCClient(url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput
        else:
            raise ValueError(
                f"Unsupported scheme: {scheme}. Use 'http' or 'grpc'.")

        model_metadata = self.triton_client.get_model_metadata(endpoint)
        self.input_names = [input.name for input in model_metadata.inputs]
        self.output_names = [output.name for output in model_metadata.outputs]
        self.input_formats = [
            input.datatype for input in model_metadata.inputs]
        self.np_input_formats = [self._triton_to_numpy_dtype(
            dtype) for dtype in self.input_formats]

    def _parse_url(self, url: str) -> tuple:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        scheme = parsed.scheme
        netloc = parsed.netloc
        path = parsed.path.strip('/').split('/')
        endpoint = path[0] if path else ''
        return scheme, netloc, endpoint, path[1:]

    def _triton_to_numpy_dtype(self, dtype: str) -> type:
        dtype_map = {
            'BOOL': np.bool_,
            'UINT8': np.uint8,
            'UINT16': np.uint16,
            'UINT32': np.uint32,
            'UINT64': np.uint64,
            'INT8': np.int8,
            'INT16': np.int16,
            'INT32': np.int32,
            'INT64': np.int64,
            'FP16': np.float16,
            'FP32': np.float32,
            'FP64': np.float64,
            'BYTES': np.object_,
        }
        return dtype_map.get(dtype, np.object_)

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        '''
        Call the model with the given inputs.
        Args:
            *inputs (List[np.ndarray]): Input data to the model.
        Returns:
            (List[np.ndarray]): Model outputs.
        '''
        if len(inputs) != len(self.input_names):
            raise ValueError(
                f"Expected {len(self.input_names)} inputs, got {len(inputs)}")

        infer_inputs = []
        for name, input_data, dtype in zip(self.input_names, inputs, self.np_input_formats):
            infer_input = self.InferInput(name, input_data.shape, dtype)
            infer_input.set_data_from_numpy(input_data)
            infer_inputs.append(infer_input)

        infer_outputs = [self.InferRequestedOutput(
            name) for name in self.output_names]

        response = self.triton_client.infer(
            model_name=self.endpoint,
            inputs=infer_inputs,
            outputs=infer_outputs
        )

        return [response.as_numpy(name) for name in self.output_names]
