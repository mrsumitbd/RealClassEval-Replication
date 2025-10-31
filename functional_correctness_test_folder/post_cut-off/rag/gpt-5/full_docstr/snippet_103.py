import numpy as np
from typing import List, Optional, Tuple
from urllib.parse import urlsplit


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
        try:
            import tritonclient.http as triton_http
            import tritonclient.grpc as triton_grpc
        except Exception as e:
            raise ImportError(
                'tritonclient package is required to use TritonRemoteModel') from e

        parsed_scheme, netloc, parsed_endpoint = self._parse_url(url)

        if not scheme:
            scheme = parsed_scheme or 'http'
        self.scheme = scheme.lower()

        # Explicit endpoint overrides parsed one
        self.endpoint = endpoint or parsed_endpoint
        if not self.endpoint:
            raise ValueError(
                'Triton model endpoint (name) could not be determined.')

        # Build base server URL for client initialization
        if self.scheme == 'grpc':
            base_url = netloc
            self.triton_client = triton_grpc.InferenceServerClient(
                url=base_url)
            self.InferInput = triton_grpc.InferInput
            self.InferRequestedOutput = triton_grpc.InferRequestedOutput
            self.url = base_url
        else:
            # default to HTTP (allow https if provided)
            http_scheme = 'http' if self.scheme not in (
                'http', 'https') else self.scheme
            base_url = f'{http_scheme}://{netloc}'
            self.triton_client = triton_http.InferenceServerClient(
                url=base_url)
            self.InferInput = triton_http.InferInput
            self.InferRequestedOutput = triton_http.InferRequestedOutput
            self.url = base_url

        # Populate model metadata
        self.input_formats: List[str] = []
        self.np_input_formats: List[type] = []
        self.input_names: List[str] = []
        self.output_names: List[str] = []
        self._refresh_metadata()

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        '''
        Call the model with the given inputs.
        Args:
            *inputs (List[np.ndarray]): Input data to the model.
        Returns:
            (List[np.ndarray]): Model outputs.
        '''
        if not inputs:
            raise ValueError('At least one input is required.')

        if self.input_names and len(inputs) != len(self.input_names):
            raise ValueError(
                f'Expected {len(self.input_names)} inputs, got {len(inputs)}.')

        infer_inputs = []
        for idx, arr in enumerate(inputs):
            name = self.input_names[idx] if idx < len(
                self.input_names) else f'INPUT{idx}'
            dtype_triton = self.input_formats[idx] if idx < len(
                self.input_formats) else self._numpy_to_triton_dtype(arr.dtype)
            np_target_dtype = self._triton_to_numpy_dtype(dtype_triton)
            if np_target_dtype is not None and arr.dtype != np_target_dtype:
                arr = arr.astype(np_target_dtype, copy=False)

            ii = self.InferInput(name, list(arr.shape), dtype_triton)
            # HTTP supports binary_data flag; gRPC doesn't
            try:
                ii.set_data_from_numpy(arr, binary_data=True)  # HTTP path
            except TypeError:
                ii.set_data_from_numpy(arr)  # gRPC path
            infer_inputs.append(ii)

        infer_outputs = []
        for name in self.output_names:
            try:
                infer_outputs.append(self.InferRequestedOutput(
                    name, binary_data=True))  # HTTP path
            except TypeError:
                infer_outputs.append(
                    self.InferRequestedOutput(name))  # gRPC path

        result = self.triton_client.infer(
            model_name=self.endpoint, inputs=infer_inputs, outputs=infer_outputs)

        outputs = []
        for name in self.output_names:
            outputs.append(result.as_numpy(name))
        return outputs

    # --------------- Helpers ---------------

    def _parse_url(self, url: str) -> Tuple[Optional[str], str, str]:
        scheme = None
        netloc = ''
        endpoint = ''

        if '://' in url:
            parts = urlsplit(url)
            scheme = parts.scheme or None
            netloc = parts.netloc
            path = parts.path.lstrip('/')
        else:
            # Accept forms like "host:port/model" or "host:port"
            tmp = url.strip('/')
            segs = tmp.split('/', 1)
            netloc = segs[0]
            path = segs[1] if len(segs) > 1 else ''

        if path:
            endpoint = path.split('/', 1)[0]

        if not netloc:
            # handle malformed input like "http://model" without host:port
            # or just "model" string
            if path:
                netloc = path
                endpoint = ''
            elif url:
                netloc = url

        return scheme, netloc, endpoint

    def _refresh_metadata(self) -> None:
        md = self.triton_client.get_model_metadata(self.endpoint)
        if isinstance(md, dict):
            # HTTP json response
            inps = md.get('inputs', [])
            outs = md.get('outputs', [])
            self.input_names = [i.get('name') for i in inps]
            self.input_formats = [i.get('datatype') for i in inps]
            self.output_names = [o.get('name') for o in outs]
        else:
            # gRPC response object
            self.input_names = [i.name for i in getattr(md, 'inputs', [])]
            self.input_formats = [
                i.datatype for i in getattr(md, 'inputs', [])]
            self.output_names = [o.name for o in getattr(md, 'outputs', [])]

        self.np_input_formats = [self._triton_to_numpy_dtype(
            dt) for dt in self.input_formats]

    def _triton_to_numpy_dtype(self, dtype: Optional[str]) -> Optional[np.dtype]:
        if dtype is None:
            return None
        dtype = dtype.upper()
        mapping = {
            'BOOL': np.bool_,
            'INT8': np.int8,
            'INT16': np.int16,
            'INT32': np.int32,
            'INT64': np.int64,
            'UINT8': np.uint8,
            'UINT16': np.uint16,
            'UINT32': np.uint32,
            'UINT64': np.uint64,
            'FP8': np.uint8,       # best-effort fallback
            'FP16': np.float16,
            'BF16': getattr(np, 'bfloat16', np.float16),
            'FP32': np.float32,
            'FP64': np.float64,
            'BYTES': np.object_,
            'INT4': np.uint8,      # pack/unpack not handled, best-effort
            'UINT4': np.uint8,     # pack/unpack not handled, best-effort
        }
        return mapping.get(dtype, None)

    def _numpy_to_triton_dtype(self, dtype: np.dtype) -> str:
        dtype = np.dtype(dtype)
        reverse = {
            np.bool_: 'BOOL',
            np.int8: 'INT8',
            np.int16: 'INT16',
            np.int32: 'INT32',
            np.int64: 'INT64',
            np.uint8: 'UINT8',
            np.uint16: 'UINT16',
            np.uint32: 'UINT32',
            np.uint64: 'UINT64',
            np.float16: 'FP16',
            getattr(np, 'bfloat16', type('BFLOAT16_PLACEHOLDER', (), {})): 'BF16',
            np.float32: 'FP32',
            np.float64: 'FP64',
            np.object_: 'BYTES',
        }
        for k, v in reverse.items():
            try:
                if dtype == np.dtype(k):
                    return v
            except TypeError:
                # placeholder type won't be convertible to dtype
                continue
        return 'BYTES'
