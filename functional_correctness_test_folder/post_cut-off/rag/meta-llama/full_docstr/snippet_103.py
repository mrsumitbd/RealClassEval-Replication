
from typing import List
import numpy as np
from tritonclient.http import InferenceServerClient, InferInput, InferRequestedOutput
from tritonclient.grpc import InferenceServerClient as grpcInferenceServerClient
from tritonclient.grpc import InferInput as grpcInferInput
from tritonclient.grpc import InferRequestedOutput as grpcInferRequestedOutput
from urllib.parse import urlparse


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
            parsed_url = urlparse(url)
            scheme = parsed_url.scheme
            endpoint = parsed_url.path.strip('/')
            url = parsed_url.netloc

        self.url = url
        self.endpoint = endpoint

        if scheme == 'http':
            self.triton_client = InferenceServerClient(url=self.url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput
        elif scheme == 'grpc':
            self.triton_client = grpcInferenceServerClient(url=self.url)
            self.InferInput = grpcInferInput
            self.InferRequestedOutput = grpcInferRequestedOutput
        else:
            raise ValueError(
                "Invalid scheme. Supported schemes are 'http' and 'grpc'.")

        model_metadata = self.triton_client.get_model_metadata(
            model_name=self.endpoint)
        self.input_formats = [input['data_type']
                              for input in model_metadata.inputs]
        self.np_input_formats = [self._triton_dtype_to_np_dtype(
            input_format) for input_format in self.input_formats]
        self.input_names = [input['name'] for input in model_metadata.inputs]
        self.output_names = [output['name']
                             for output in model_metadata.outputs]

    def _triton_dtype_to_np_dtype(self, triton_dtype: str) -> np.dtype:
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
        return dtype_map.get(triton_dtype, np.object_)

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
                f"Expected {len(self.input_names)} inputs, but got {len(inputs)}")

        infer_inputs = []
        for i, input_data in enumerate(inputs):
            if input_data.dtype != self.np_input_formats[i]:
                input_data = input_data.astype(self.np_input_formats[i])
            infer_input = self.InferInput(
                self.input_names[i], input_data.shape, self.input_formats[i])
            infer_input.set_data_from_numpy(input_data)
            infer_inputs.append(infer_input)

        infer_outputs = [self.InferRequestedOutput(
            output_name) for output_name in self.output_names]

        response = self.triton_client.infer(
            model_name=self.endpoint, inputs=infer_inputs, outputs=infer_outputs)

        return [response.as_numpy(output_name) for output_name in self.output_names]
