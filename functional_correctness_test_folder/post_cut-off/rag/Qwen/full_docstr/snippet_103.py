
import numpy as np
import tritonclient.http as httpclient
import tritonclient.grpc as grpcclient
from tritonclient.utils import InferenceServerException
from urllib.parse import urlparse
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
        parsed_url = urlparse(url)
        if scheme:
            self.scheme = scheme
        else:
            self.scheme = parsed_url.scheme

        if endpoint:
            self.endpoint = endpoint
        else:
            self.endpoint = parsed_url.path.strip('/').split('/')[-1]

        self.url = f"{parsed_url.netloc}{parsed_url.path.strip('/')}"
        if self.scheme == 'http':
            self.triton_client = httpclient.InferenceServerClient(self.url)
            self.InferInput = httpclient.InferInput
            self.InferRequestedOutput = httpclient.InferRequestedOutput
        elif self.scheme == 'grpc':
            self.triton_client = grpcclient.InferenceServerClient(self.url)
            self.InferInput = grpcclient.InferInput
            self.InferRequestedOutput = grpcclient.InferRequestedOutput
        else:
            raise ValueError("Unsupported scheme. Use 'http' or 'grpc'.")

        self.input_formats = []
        self.np_input_formats = []
        self.input_names = []
        self.output_names = []

        model_metadata = self.triton_client.get_model_metadata(self.endpoint)
        for input_metadata in model_metadata['inputs']:
            self.input_names.append(input_metadata['name'])
            self.input_formats.append(input_metadata['datatype'])
            self.np_input_formats.append(
                self._triton_to_numpy_dtype(input_metadata['datatype']))

        for output_metadata in model_metadata['outputs']:
            self.output_names.append(output_metadata['name'])

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

        triton_inputs = []
        for input_name, input_data, np_dtype in zip(self.input_names, inputs, self.np_input_formats):
            triton_input = self.InferInput(
                input_name, input_data.shape, self._numpy_to_triton_dtype(np_dtype))
            triton_input.set_data_from_numpy(input_data.astype(np_dtype))
            triton_inputs.append(triton_input)

        triton_outputs = [self.InferRequestedOutput(
            output_name) for output_name in self.output_names]

        try:
            results = self.triton_client.infer(
                self.endpoint, inputs=triton_inputs, outputs=triton_outputs)
        except InferenceServerException as e:
            raise RuntimeError(f"Failed to run inference: {e}")

        outputs = [results.as_numpy(output_name)
                   for output_name in self.output_names]
        return outputs

    @staticmethod
    def _triton_to_numpy_dtype(triton_dtype: str) -> type:
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
            'FP128': np.float128,
            # Note: BF16 is not directly supported in numpy, using float16 as a placeholder
            'BF16': np.float16,
        }
        return dtype_map.get(triton_dtype, np.float32)

    @staticmethod
    def _numpy_to_triton_dtype(np_dtype: type) -> str:
        dtype_map = {
            np.bool_: 'BOOL',
            np.uint8: 'UINT8',
            np.uint16: 'UINT16',
            np.uint32: 'UINT32',
            np.uint64: 'UINT64',
            np.int8: 'INT8',
            np.int16: 'INT16',
            np.int32: 'INT32',
            np.int64: 'INT64',
            np.float16: 'FP16',
            np.float32: 'FP32',
            np.float64: 'FP64',
            np.float128: 'FP128',
        }
        return dtype_map.get(np_dtype, 'FP32')
