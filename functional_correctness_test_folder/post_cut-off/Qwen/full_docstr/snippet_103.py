
import numpy as np
from tritonclient.http import InferenceServerClient as HttpClient
from tritonclient.http import InferInput, InferRequestedOutput
from tritonclient.grpc import InferenceServerClient as GrpcClient
from typing import List, Union


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
        if '://' in url:
            scheme, url = url.split('://')
            url, endpoint = url.split('/', 1)
            endpoint = endpoint.rstrip('/')

        self.url = url
        self.endpoint = endpoint
        self.scheme = scheme.lower()

        if self.scheme == 'http':
            self.triton_client = HttpClient(self.url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput
        elif self.scheme == 'grpc':
            self.triton_client = GrpcClient(self.url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput
        else:
            raise ValueError("Scheme must be 'http' or 'grpc'.")

        model_metadata = self.triton_client.get_model_metadata(self.endpoint)
        self.input_formats = [input_config['data_type']
                              for input_config in model_metadata['inputs']]
        self.np_input_formats = [self._triton_to_numpy_dtype(
            dtype) for dtype in self.input_formats]
        self.input_names = [input_config['name']
                            for input_config in model_metadata['inputs']]
        self.output_names = [output_config['name']
                             for output_config in model_metadata['outputs']]

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
                f"Expected {len(self.input_names)} inputs, but got {len(inputs)}.")

        infer_inputs = []
        for input_name, input_data, input_format in zip(self.input_names, inputs, self.np_input_formats):
            infer_input = self.InferInput(
                input_name, input_data.shape, input_format)
            infer_input.set_data_from_numpy(input_data)
            infer_inputs.append(infer_input)

        infer_outputs = [self.InferRequestedOutput(
            output_name) for output_name in self.output_names]

        results = self.triton_client.infer(
            self.endpoint, inputs=infer_inputs, outputs=infer_outputs)
        return [results.as_numpy(output_name) for output_name in self.output_names]

    @staticmethod
    def _triton_to_numpy_dtype(dtype: str) -> str:
        dtype_map = {
            'TYPE_BOOL': '?',
            'TYPE_UINT8': 'u1',
            'TYPE_UINT16': 'u2',
            'TYPE_UINT32': 'u4',
            'TYPE_UINT64': 'u8',
            'TYPE_INT8': 'i1',
            'TYPE_INT16': 'i2',
            'TYPE_INT32': 'i4',
            'TYPE_INT64': 'i8',
            'TYPE_FP16': 'f2',
            'TYPE_FP32': 'f4',
            'TYPE_FP64': 'f8',
            'TYPE_STRING': 'object'
        }
        return dtype_map.get(dtype, dtype)
