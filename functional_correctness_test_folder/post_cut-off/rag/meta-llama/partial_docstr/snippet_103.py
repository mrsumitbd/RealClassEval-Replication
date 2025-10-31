
from typing import List
import numpy as np
from urllib.parse import urlparse
import tritonclient.http as httpclient
import tritonclient.grpc as grpcclient


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
        if not endpoint and not scheme:
            parsed_url = urlparse(url)
            scheme = parsed_url.scheme
            endpoint = parsed_url.path.strip('/')
            url = parsed_url.netloc
        if scheme == 'http':
            self.triton_client = httpclient.InferenceServerClient(url=url)
            self.InferInput = httpclient.InferInput
            self.InferRequestedOutput = httpclient.InferRequestedOutput
        elif scheme == 'grpc':
            self.triton_client = grpcclient.InferenceServerClient(url=url)
            self.InferInput = grpcclient.InferInput
            self.InferRequestedOutput = grpcclient.InferRequestedOutput
        else:
            raise ValueError(f"Unsupported scheme: {scheme}")
        self.url = url
        self.endpoint = endpoint
        self.input_names = [f'INPUT{i}' for i in range(
            len(self.triton_client.get_model_config(endpoint)['input']))]
        self.output_names = [f'OUTPUT{i}' for i in range(
            len(self.triton_client.get_model_config(endpoint)['output']))]
        self.input_formats = [self.triton_client.get_model_config(endpoint)['input'][i]['data_type'] for i in range(
            len(self.triton_client.get_model_config(endpoint)['input']))]
        self.np_input_formats = [
            self._triton_to_np_dtype(f) for f in self.input_formats]

    def _triton_to_np_dtype(self, triton_dtype: str) -> np.dtype:
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
            'BYTES': np.object_
        }
        return dtype_map.get(triton_dtype, np.float32)

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        '''
        Call the model with the given inputs.
        Args:
            *inputs (List[np.ndarray]): Input data to the model.
        Returns:
            (List[np.ndarray]): Model outputs.
        '''
        inputs = [self.InferInput(name, input.shape, self._np_to_triton_dtype(
            input.dtype)) for name, input in zip(self.input_names, inputs)]
        for input, data in zip(inputs, inputs):
            input.set_data_from_numpy(data)
        outputs = [self.InferRequestedOutput(
            name) for name in self.output_names]
        response = self.triton_client.infer(
            model_name=self.endpoint, inputs=inputs, outputs=outputs)
        return [response.as_numpy(name) for name in self.output_names]

    def _np_to_triton_dtype(self, np_dtype: np.dtype) -> str:
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
            np.object_: 'BYTES'
        }
        return dtype_map.get(np_dtype, 'FP32')
