import numpy as np
from typing import List
from urllib.parse import urlparse
import importlib


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
        # Parse url if needed
        parsed = urlparse(url)
        if parsed.scheme and parsed.netloc:
            self.scheme = parsed.scheme
            self.url = f"{parsed.scheme}://{parsed.netloc}"
            # endpoint is the first path component
            path_parts = parsed.path.lstrip('/').split('/')
            self.endpoint = path_parts[0] if path_parts and path_parts[0] else endpoint
        else:
            self.url = url
            self.endpoint = endpoint
            self.scheme = scheme or 'http'

        # Select client and classes
        if self.scheme == 'grpc':
            triton_module = importlib.import_module('tritonclient.grpc')
            self.triton_client = triton_module.InferenceServerClient(
                url=self.url)
            self.InferInput = triton_module.InferInput
            self.InferRequestedOutput = triton_module.InferRequestedOutput
        else:
            triton_module = importlib.import_module('tritonclient.http')
            self.triton_client = triton_module.InferenceServerClient(
                url=self.url)
            self.InferInput = triton_module.InferInput
            self.InferRequestedOutput = triton_module.InferRequestedOutput

        # Get model metadata
        model_metadata = self.triton_client.get_model_metadata(self.endpoint)
        model_config = self.triton_client.get_model_config(self.endpoint)

        self.input_names = [inp['name'] for inp in model_metadata['inputs']]
        self.output_names = [out['name'] for out in model_metadata['outputs']]
        self.input_formats = [inp['datatype']
                              for inp in model_metadata['inputs']]

        # Map Triton datatypes to numpy dtypes
        triton_to_np = {
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
            'STRING': np.object_,
        }
        self.np_input_formats = [triton_to_np.get(
            dt, np.float32) for dt in self.input_formats]

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        '''
        Call the model with the given inputs.
        Args:
            *inputs (List[np.ndarray]): Input data to the model.
        Returns:
            (List[np.ndarray]): Model outputs.
        '''
        infer_inputs = []
        for i, (name, dtype) in enumerate(zip(self.input_names, self.input_formats)):
            arr = inputs[i]
            infer_input = self.InferInput(name, arr.shape, dtype)
            infer_input.set_data_from_numpy(arr)
            infer_inputs.append(infer_input)

        infer_outputs = [self.InferRequestedOutput(
            name) for name in self.output_names]

        results = self.triton_client.infer(
            self.endpoint,
            inputs=infer_inputs,
            outputs=infer_outputs
        )

        output_arrays = []
        for name in self.output_names:
            output = results.as_numpy(name)
            output_arrays.append(output)
        return output_arrays
