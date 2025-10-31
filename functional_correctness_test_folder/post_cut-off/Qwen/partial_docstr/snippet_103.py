
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

    def __init__(self, url: str, endpoint: str = '', scheme: str = 'http'):
        self.url = url
        self.endpoint = endpoint
        self.scheme = scheme
        self.triton_client = HttpClient(
            url) if scheme == 'http' else GrpcClient(url)
        self.InferInput = InferInput if scheme == 'http' else GrpcClient.InferInput
        self.InferRequestedOutput = InferRequestedOutput if scheme == 'http' else GrpcClient.InferRequestedOutput
        self.input_formats = []
        self.np_input_formats = []
        self.input_names = []
        self.output_names = []
        self._initialize_model_metadata()

    def _initialize_model_metadata(self):
        model_metadata = self.triton_client.get_model_metadata(self.endpoint)
        self.input_formats = [
            input.metadata.datatype for input in model_metadata.inputs]
        self.np_input_formats = [self._triton_to_numpy_dtype(
            dtype) for dtype in self.input_formats]
        self.input_names = [input.name for input in model_metadata.inputs]
        self.output_names = [output.name for output in model_metadata.outputs]

    @staticmethod
    def _triton_to_numpy_dtype(dtype: str) -> type:
        dtype_map = {
            'TYPE_FP32': np.float32,
            'TYPE_FP16': np.float16,
            'TYPE_INT32': np.int32,
            'TYPE_INT8': np.int8,
            'TYPE_UINT8': np.uint8,
            'TYPE_INT64': np.int64,
            'TYPE_BOOL': np.bool_,
        }
        return dtype_map.get(dtype, np.float32)

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        if len(inputs) != len(self.input_names):
            raise ValueError(
                f"Expected {len(self.input_names)} inputs, but got {len(inputs)}")

        infer_inputs = []
        for name, input_data, np_dtype in zip(self.input_names, inputs, self.np_input_formats):
            infer_input = self.InferInput(
                name, input_data.shape, self._numpy_to_triton_dtype(np_dtype))
            infer_input.set_data_from_numpy(input_data.astype(np_dtype))
            infer_inputs.append(infer_input)

        infer_outputs = [self.InferRequestedOutput(
            name) for name in self.output_names]
        results = self.triton_client.infer(
            self.endpoint, inputs=infer_inputs, outputs=infer_outputs)
        return [results.as_numpy(name) for name in self.output_names]

    @staticmethod
    def _numpy_to_triton_dtype(dtype: type) -> str:
        dtype_map = {
            np.float32: 'FP32',
            np.float16: 'FP16',
            np.int32: 'INT32',
            np.int8: 'INT8',
            np.uint8: 'UINT8',
            np.int64: 'INT64',
            np.bool_: 'BOOL',
        }
        return dtype_map.get(dtype, 'FP32')
