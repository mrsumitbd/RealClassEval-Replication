
import numpy as np
from typing import List, Optional
from urllib.parse import urlparse
import tritonclient.http as httpclient
import tritonclient.grpc as grpcclient

# Mapping between Triton data types and NumPy dtypes
TRITON_TO_NP = {
    'INT8': np.int8,
    'UINT8': np.uint8,
    'INT16': np.int16,
    'UINT16': np.uint16,
    'INT32': np.int32,
    'UINT32': np.uint32,
    'INT64': np.int64,
    'UINT64': np.uint64,
    'FP16': np.float16,
    'FP32': np.float32,
    'FP64': np.float64,
    'BOOL': np.bool_,
    'BYTES': np.object_,
}

# Reverse mapping from NumPy dtype to Triton data type string
NP_TO_TRITON = {
    np.dtype('int8'): 'INT8',
    np.dtype('uint8'): 'UINT8',
    np.dtype('int16'): 'INT16',
    np.dtype('uint16'): 'UINT16',
    np.dtype('int32'): 'INT32',
    np.dtype('uint32'): 'UINT32',
    np.dtype('int64'): 'INT64',
    np.dtype('uint64'): 'UINT64',
    np.dtype('float16'): 'FP16',
    np.dtype('float32'): 'FP32',
    np.dtype('float64'): 'FP64',
    np.dtype('bool'): 'BOOL',
    np.dtype('object'): 'BYTES',
}


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
        # Parse URL if needed
        parsed = urlparse(url)
        self.url = parsed.scheme + '://' + parsed.netloc
        if not scheme:
            scheme = parsed.scheme
        if not endpoint:
            # first non-empty path component is the endpoint
            parts = [p for p in parsed.path.split('/') if p]
            endpoint = parts[0] if parts else ''
        self.endpoint = endpoint
        self.scheme = scheme

        # Create Triton client and helper classes
        if scheme == 'http':
            self.triton_client = httpclient.InferenceServerClient(
                url=parsed.netloc)
            self.InferInput = httpclient.InferInput
            self.InferRequestedOutput = httpclient.InferRequestedOutput
        elif scheme == 'grpc':
            self.triton_client = grpcclient.InferenceServerClient(
                url=parsed.netloc)
            self.InferInput = grpcclient.InferInput
            self.InferRequestedOutput = grpcclient.InferRequestedOutput
        else:
            raise ValueError(
                f"Unsupported scheme '{scheme}'. Use 'http' or 'grpc'.")

        # Retrieve model metadata
        metadata = self.triton_client.get_model_metadata(
            model_name=self.endpoint)
        self.input_names = [inp['name'] for inp in metadata['inputs']]
        self.input_formats = [inp['datatype'] for inp in metadata['inputs']]
        self.np_input_formats = [TRITON_TO_NP.get(
            dt, np.object_) for dt in self.input_formats]
        self.output_names = [out['name'] for out in metadata['outputs']]

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
                f"Expected {len(self.input_names)} inputs, got {len(inputs)}.")

        # Build InferInput objects
        triton_inputs = []
        for name, arr in
