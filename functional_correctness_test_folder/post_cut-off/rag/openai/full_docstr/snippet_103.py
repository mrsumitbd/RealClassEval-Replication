
import numpy as np
from urllib.parse import urlparse
from typing import List, Optional

# Triton client imports
try:
    from tritonclient.http import InferenceServerClient as HTTPClient
    from tritonclient.http import InferInput as HTTPInferInput
    from tritonclient.http import InferRequestedOutput as HTTPInferRequestedOutput
except Exception:
    HTTPClient = None
    HTTPInferInput = None
    HTTPInferRequestedOutput = None

try:
    from tritonclient.grpc import InferenceServerClient as GRPCClient
    from tritonclient.grpc import InferInput as GRPCInferInput
    from tritonclient.grpc import InferRequestedOutput as GRPCInferRequestedOutput
except Exception:
    GRPCClient = None
    GRPCInferInput = None
    GRPCInferRequestedOutput = None

# Triton utils for datatype conversion
try:
    from tritonclient.utils import to_numpy_dtype
except Exception:
    def to_numpy_dtype(dtype: str):
        # Fallback mapping for common types
        mapping = {
            'INT8': np.int8,
            'INT16': np.int16,
            'INT32': np.int32,
            'INT64': np.int64,
            'UINT8': np.uint8,
            'UINT16': np.uint16,
            'UINT32': np.uint32,
            'UINT64': np.uint64,
            'FP16': np.float16,
            'FP32': np.float32,
            'FP64': np.float64,
            'BOOL': np.bool_,
            'BYTES': np.object_,
        }
        return mapping.get(dtype.upper(), np.object_)


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
        # Parse the URL
        parsed = urlparse(url)
        if not scheme:
            scheme = parsed.scheme or 'http'
        if not endpoint:
            # Extract first non-empty path segment as endpoint
            path_parts = [p for p in parsed.path.split('/') if p]
            if path_parts:
                endpoint = path_parts[0]
            else:
                raise ValueError(
                    'Endpoint must be specified either as argument or in URL path')
        # Store attributes
        self.endpoint = endpoint
        self.url = f'{scheme}://{parsed.netloc}'
        self.scheme = scheme.lower()

        # Create Triton client
        if self.scheme == 'http':
            if HTTPClient is None:
                raise ImportError('tritonclient.http is not available')
            self.triton_client = HTTPClient(url=parsed.netloc, verbose=False)
            self.InferInput = HTTPInferInput
            self.InferRequestedOutput = HTTPInferRequestedOutput
        elif self.scheme == 'grpc':
            if GRPCClient is None:
                raise ImportError('tritonclient.grpc is not available')
            self.triton_client = GRPCClient(url=parsed.netloc, verbose=False)
            self.InferInput = GRPCInferInput
            self.InferRequestedOutput = GRPCInferRequestedOutput
        else:
            raise ValueError(f'Unsupported scheme: {self.scheme}')

        # Retrieve model metadata
        metadata = self.triton_client.get_model_metadata(self.endpoint)
        self.input_names = [inp['name'] for inp in metadata['inputs']]
        self.input_formats = [inp['datatype'] for inp in metadata['inputs']]
        self.np_input_formats = [to_numpy_dtype(
            dt) for dt in self.input_formats]
        self.output_names = [out['name'] for out in metadata['outputs']]

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        '''
        Call the model with the given inputs.
