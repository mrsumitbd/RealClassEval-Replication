import numpy as np
from typing import List, Tuple, Optional
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
        self.endpoint: str = ''
        self.url: str = ''
        self.triton_client = None
        self.InferInput = None
        self.InferRequestedOutput = None
        self.input_formats: List[str] = []
        self.np_input_formats: List[np.dtype] = []
        self.input_names: List[str] = []
        self.output_names: List[str] = []

        parsed = urlparse(
            url if '://' in url else f'{scheme or "http"}://{url}')
        parsed_scheme = parsed.scheme or scheme or 'http'
        if scheme and scheme.lower() not in ('http', 'grpc'):
            raise ValueError("scheme must be either 'http' or 'grpc'")
        scheme_final = (scheme or parsed_scheme).lower()
        if scheme_final not in ('http', 'grpc'):
            scheme_final = 'http'

        # Endpoint resolution
        endpoint_final = endpoint or (
            parsed.path.strip('/').split('/')[:1] or [''])[0]
        if not endpoint_final:
            raise ValueError(
                "endpoint (model name) must be provided either as an argument or in the URL path")

        # Server URL handling for client constructors
        netloc = parsed.netloc or parsed.path.split('/')[0]
        if not netloc:
            raise ValueError(
                "Invalid URL; could not determine server host:port")
        # Store human-friendly url
        self.url = f"{scheme_final}://{netloc}"
        self.endpoint = endpoint_final

        # Create client
        try:
            if scheme_final == 'http':
                from tritonclient.http import InferenceServerClient, InferInput as HTTPInferInput, InferRequestedOutput as HTTPInferRequestedOutput
                self.triton_client = InferenceServerClient(url=self.url)
                self.InferInput = HTTPInferInput
                self.InferRequestedOutput = HTTPInferRequestedOutput
                metadata = self.triton_client.get_model_metadata(
                    model_name=self.endpoint)
                inputs_meta, outputs_meta = self._normalize_metadata(
                    metadata, is_grpc=False)
            else:
                from tritonclient.grpc import InferenceServerClient, InferInput as GRPCInferInput, InferRequestedOutput as GRPCInferRequestedOutput
                # grpc client expects host:port (no scheme)
                self.triton_client = InferenceServerClient(url=netloc)
                self.InferInput = GRPCInferInput
                self.InferRequestedOutput = GRPCInferRequestedOutput
                metadata = self.triton_client.get_model_metadata(
                    model_name=self.endpoint)
                inputs_meta, outputs_meta = self._normalize_metadata(
                    metadata, is_grpc=True)
        except ImportError as e:
            raise ImportError(
                "tritonclient is required. Install with: pip install 'tritonclient[all]'") from e

        # Extract names and datatypes
        self.input_names = [i['name'] for i in inputs_meta]
        self.output_names = [o['name'] for o in outputs_meta]
        self.input_formats = [i['datatype'] for i in inputs_meta]
        self.np_input_formats = [self._triton_dtype_to_numpy(
            dt) for dt in self.input_formats]

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        '''
        Call the model with the given inputs.
        Args:
            *inputs (List[np.ndarray]): Input data to the model.
        Returns:
            (List[np.ndarray]): Model outputs.
        '''
        if not inputs:
            raise ValueError("At least one input array must be provided")
        if len(inputs) != len(self.input_names):
            raise ValueError(
                f"Model expects {len(self.input_names)} inputs ({self.input_names}); got {len(inputs)}")

        prepared_inputs = []
        for idx, (name, triton_dtype, np_dtype_expected, arr) in enumerate(
            zip(self.input_names, self.input_formats,
                self.np_input_formats, inputs)
        ):
            if not isinstance(arr, np.ndarray):
                arr = np.asarray(arr)
            # Cast if needed
            if np_dtype_expected is not None and arr.dtype != np_dtype_expected:
                try:
                    arr = arr.astype(np_dtype_expected, copy=False)
                except TypeError:
                    # As a fallback for types like BYTES/object leave as is
                    pass
            inp = self.InferInput(name=name, shape=list(
                arr.shape), datatype=triton_dtype)
            inp.set_data_from_numpy(arr)
            prepared_inputs.append(inp)

        requested_outputs = [self.InferRequestedOutput(
            n) for n in self.output_names]
        result = self.triton_client.infer(
            model_name=self.endpoint, inputs=prepared_inputs, outputs=requested_outputs)

        outputs = [result.as_numpy(name) for name in self.output_names]
        return outputs

    @staticmethod
    def _normalize_metadata(metadata, is_grpc: bool) -> Tuple[List[dict], List[dict]]:
        if is_grpc:
            # grpc returns a ModelMetadataResponse
            inputs = [{'name': i.name, 'datatype': i.datatype,
                       'shape': list(i.shape)} for i in metadata.inputs]
            outputs = [{'name': o.name, 'datatype': o.datatype,
                        'shape': list(o.shape)} for o in metadata.outputs]
        else:
            # http returns dict
            inputs = [{'name': i['name'], 'datatype': i['datatype'], 'shape': i.get(
                'shape', [])} for i in metadata.get('inputs', [])]
            outputs = [{'name': o['name'], 'datatype': o['datatype'], 'shape': o.get(
                'shape', [])} for o in metadata.get('outputs', [])]
        return inputs, outputs

    @staticmethod
    def _triton_dtype_to_numpy(dtype: str) -> Optional[np.dtype]:
        mapping = {
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
        }
        if dtype == 'BF16':
            bfloat = getattr(np, 'bfloat16', None)
            if bfloat is None:
                raise TypeError(
                    "NumPy does not support bfloat16 on this installation, required by model input")
            return bfloat
        if dtype not in mapping:
            # Unknown type; let Triton try to handle it
            return None
        return mapping[dtype]
