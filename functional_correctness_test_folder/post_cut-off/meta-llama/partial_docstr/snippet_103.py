
import numpy as np
from typing import List
import tritonclient.http as httpclient
import tritonclient.grpc as grpcclient
from tritonclient.utils import *


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

    def __init__(self, url: str, endpoint: str = '', scheme: str = 'http'):
        if scheme == 'http':
            self.triton_client = httpclient.InferenceServerClient(url=url)
            self.InferInput = httpclient.InferInput
            self.InferRequestedOutput = httpclient.InferRequestedOutput
        elif scheme == 'grpc':
            self.triton_client = grpcclient.InferenceServerClient(url=url)
            self.InferInput = grpcclient.InferInput
            self.InferRequestedOutput = grpcclient.InferRequestedOutput
        else:
            raise ValueError(
                "Invalid scheme. Supported schemes are 'http' and 'grpc'.")

        self.url = url
        self.endpoint = endpoint

        model_metadata = self.triton_client.get_model_metadata(
            model_name=endpoint)
        model_config = self.triton_client.get_model_config(model_name=endpoint)

        self.input_names = [input.name for input in model_metadata.inputs]
        self.output_names = [output.name for output in model_metadata.outputs]

        self.input_formats = [
            input.data_type for input in model_config.config.input]
        self.np_input_formats = [self._triton_dtype_to_np_dtype(
            dtype) for dtype in self.input_formats]

    def _triton_dtype_to_np_dtype(self, dtype: str) -> type:
        dtype_map = {
            'TYPE_BOOL': np.bool_,
            'TYPE_UINT8': np.uint8,
            'TYPE_UINT16': np.uint16,
            'TYPE_UINT32': np.uint32,
            'TYPE_UINT64': np.uint64,
            'TYPE_INT8': np.int8,
            'TYPE_INT16': np.int16,
            'TYPE_INT32': np.int32,
            'TYPE_INT64': np.int64,
            'TYPE_FP16': np.float16,
            'TYPE_FP32': np.float32,
            'TYPE_FP64': np.float64,
            'TYPE_STRING': np.object_,
        }
        return dtype_map[dtype]

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        if len(inputs) != len(self.input_names):
            raise ValueError(
                f"Expected {len(self.input_names)} inputs, but got {len(inputs)}")

        for i, (input, name, dtype) in enumerate(zip(inputs, self.input_names, self.np_input_formats)):
            if input.dtype != dtype:
                raise ValueError(
                    f"Input {i} ({name}) has incorrect dtype. Expected {dtype}, but got {input.dtype}")

        inputs = [self.InferInput(name, input.shape, self._np_dtype_to_triton_dtype(
            input.dtype)) for name, input in zip(self.input_names, inputs)]
        for input, data in zip(inputs, inputs):
            input.set_data_from_numpy(data)

        outputs = [self.InferRequestedOutput(
            name) for name in self.output_names]

        response = self.triton_client.infer(
            model_name=self.endpoint, inputs=inputs, outputs=outputs)

        return [response.as_numpy(name) for name in self.output_names]

    def _np_dtype_to_triton_dtype(self, dtype: type) -> str:
        dtype_map = {
            np.bool_: 'TYPE_BOOL',
            np.uint8: 'TYPE_UINT8',
            np.uint16: 'TYPE_UINT16',
            np.uint32: 'TYPE_UINT32',
            np.uint64: 'TYPE_UINT64',
            np.int8: 'TYPE_INT8',
            np.int16: 'TYPE_INT16',
            np.int32: 'TYPE_INT32',
            np.int64: 'TYPE_INT64',
            np.float16: 'TYPE_FP16',
            np.float32: 'TYPE_FP32',
            np.float64: 'TYPE_FP64',
            np.object_: 'TYPE_STRING',
        }
        return dtype_map[dtype]
