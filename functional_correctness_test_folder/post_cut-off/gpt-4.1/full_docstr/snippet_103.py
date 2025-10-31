
import numpy as np
from typing import List
from urllib.parse import urlparse
import sys


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
            self.url = f"{parsed.scheme}://{parsed.netloc}"
            self.endpoint = parsed.path.strip(
                '/').split('/')[0] if not endpoint else endpoint
            self.scheme = parsed.scheme
        else:
            self.url = url
            self.endpoint = endpoint
            self.scheme = scheme if scheme else 'http'

        # Import Triton client
        if self.scheme == 'http':
            try:
                import tritonclient.http as tritonhttp
            except ImportError:
                raise ImportError(
                    "tritonclient[http] is required for HTTP scheme")
            self.triton_client = tritonhttp.InferenceServerClient(url=self.url)
            self.InferInput = tritonhttp.InferInput
            self.InferRequestedOutput = tritonhttp.InferRequestedOutput
        elif self.scheme == 'grpc':
            try:
                import tritonclient.grpc as tritongrpc
            except ImportError:
                raise ImportError(
                    "tritonclient[grpc] is required for gRPC scheme")
            self.triton_client = tritongrpc.InferenceServerClient(url=self.url)
            self.InferInput = tritongrpc.InferInput
            self.InferRequestedOutput = tritongrpc.InferRequestedOutput
        else:
            raise ValueError(f"Unsupported scheme: {self.scheme}")

        # Get model metadata
        metadata = self.triton_client.get_model_metadata(self.endpoint)
        config = self.triton_client.get_model_config(self.endpoint)
        self.input_names = [inp['name'] for inp in metadata['inputs']]
        self.output_names = [out['name'] for out in metadata['outputs']]
        self.input_formats = [inp['datatype'] for inp in metadata['inputs']]
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
        if len(inputs) != len(self.input_names):
            raise ValueError(
                f"Expected {len(self.input_names)} inputs, got {len(inputs)}")
        infer_inputs = []
        for i, (name, dtype) in enumerate(zip(self.input_names, self.input_formats)):
            arr = inputs[i]
            # Triton expects shape as list, and dtype as string
            infer_input = self.InferInput(name, arr.shape, dtype)
            infer_input.set_data_from_numpy(arr)
            infer_inputs.append(infer_input)
        infer_outputs = [self.InferRequestedOutput(
            name) for name in self.output_names]
        results = self.triton_client.infer(
            model_name=self.endpoint,
            inputs=infer_inputs,
            outputs=infer_outputs
        )
        output_arrays = []
        for name in self.output_names:
            output = results.as_numpy(name)
            output_arrays.append(output)
        return output_arrays
