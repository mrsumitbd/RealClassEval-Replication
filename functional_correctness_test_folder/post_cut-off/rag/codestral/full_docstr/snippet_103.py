
import numpy as np
from typing import List, Union
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
        if scheme:
            self.url = f"{scheme}://{url}"
        else:
            self.url = url

        if endpoint:
            self.endpoint = endpoint
        else:
            self.endpoint = url.split('/')[-1]

        if 'http' in self.url:
            self.triton_client = HTTPClient(self.url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput
        elif 'grpc' in self.url:
            self.triton_client = GRPCClient(self.url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput
        else:
            raise ValueError("Invalid scheme. Must be 'http' or 'grpc'.")

        model_metadata = self.triton_client.get_model_metadata(self.endpoint)
        self.input_formats = [input['datatype']
                              for input in model_metadata.inputs]
        self.np_input_formats = [self._get_np_dtype(
            dtype) for dtype in self.input_formats]
        self.input_names = [input['name'] for input in model_metadata.inputs]
        self.output_names = [output['name']
                             for output in model_metadata.outputs]

    def _get_np_dtype(self, dtype: str) -> type:
        dtype_map = {
            'FP32': np.float32,
            'FP64': np.float64,
            'INT8': np.int8,
            'INT16': np.int16,
            'INT32': np.int32,
            'INT64': np.int64,
            'UINT8': np.uint8,
            'UINT16': np.uint16,
            'UINT32': np.uint32,
            'UINT64': np.uint64,
            'BOOL': np.bool_
        }
        return dtype_map.get(dtype, np.float32)

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
