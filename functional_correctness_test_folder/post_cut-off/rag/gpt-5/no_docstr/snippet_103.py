from typing import List, Optional, Tuple
import numpy as np
from urllib.parse import urlparse

try:
    from tritonclient.utils import np_to_triton_dtype, triton_to_numpy_dtype
except Exception:  # pragma: no cover
    np_to_triton_dtype = None
    triton_to_numpy_dtype = None


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
        if np_to_triton_dtype is None:
            raise ImportError(
                "tritonclient is required. Install with: pip install tritonclient[all]")

        parsed = urlparse(url) if url else urlparse('')
        # Handle URLs without scheme like "localhost:8000/model"
        if not parsed.netloc and not parsed.scheme and url and '://' not in url:
            parsed = urlparse('//' + url)

        # Determine endpoint from path if not provided
        if not endpoint:
            path = (parsed.path or '').lstrip('/')
            endpoint = path.split('/', 1)[0] if path else ''

        # Determine scheme
        chosen_scheme = (scheme or parsed.scheme or 'http').lower()
        if chosen_scheme in ('https',):
            client_kind = 'http'
        elif chosen_scheme in ('grpcs',):
            client_kind = 'grpc'
        elif chosen_scheme in ('http', 'grpc'):
            client_kind = chosen_scheme
        else:
            client_kind = 'http'

        netloc = parsed.netloc or ''
        if not netloc and url:
            # Fallback if still empty (e.g., url was just "localhost:8000")
            parts = url.split('/', 1)
            netloc = parts[0]

        self.endpoint: str = endpoint
        self.url: str = f"{('http' if client_kind == 'http' else 'grpc')}://{netloc}" if netloc else ''

        # Initialize Triton client and classes
        if client_kind == 'http':
            from tritonclient.http import InferenceServerClient, InferInput, InferRequestedOutput
            base_url = f"{(parsed.scheme or 'http')}://{netloc}" if netloc else (url or '')
            self.triton_client = InferenceServerClient(url=base_url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput
        else:
            from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput
            # gRPC client expects "host:port"
            base_url = netloc or url
            # Strip possible "grpc://" prefix if present
            if base_url.startswith('grpc://'):
                base_url = base_url[len('grpc://'):]
            self.triton_client = InferenceServerClient(url=base_url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput

        # Initialize model metadata containers
        self.input_formats: List[str] = []
        self.np_input_formats: List[type] = []
        self.input_names: List[str] = []
        self.output_names: List[str] = []

        # Try to load model information (best-effort)
        try:
            self._load_model_info()
        except Exception:
            # Defer failures to call time
            pass

    def _extract_io_from_metadata(self, meta) -> Tuple[List[Tuple[str, str]], List[str]]:
        inputs_info: List[Tuple[str, str]] = []
        outputs_names: List[str] = []

        # HTTP returns dict for metadata; gRPC returns object with attributes
        if isinstance(meta, dict):
            inputs = meta.get('inputs') or meta.get('input') or []
            outputs = meta.get('outputs') or meta.get('output') or []
            for inp in inputs:
                name = inp.get('name')
                dtype = inp.get('datatype') or inp.get('data_type')
                if name and dtype:
                    inputs_info.append((name, dtype))
            for out in outputs:
                name = out.get('name')
                if name:
                    outputs_names.append(name)
        else:
            # Try attribute access (gRPC protobuf style)
            if hasattr(meta, 'inputs'):
                for inp in getattr(meta, 'inputs'):
                    name = getattr(inp, 'name', None)
                    dtype = getattr(inp, 'datatype', None) or getattr(
                        inp, 'data_type', None)
                    if name and dtype:
                        inputs_info.append((name, dtype))
            if hasattr(meta, 'outputs'):
                for out in getattr(meta, 'outputs'):
                    name = getattr(out, 'name', None)
                    if name:
                        outputs_names.append(name)

        return inputs_info, outputs_names

    def _extract_io_from_config(self, cfg) -> Tuple[List[Tuple[str, str]], List[str]]:
        inputs_info: List[Tuple[str, str]] = []
        outputs_names: List[str] = []

        # HTTP config often returned as {"config": {...}}
        if isinstance(cfg, dict):
            cfg = cfg.get('config', cfg)
            inputs = cfg.get('input', [])
            outputs = cfg.get('output', [])
            for inp in inputs:
                name = inp.get('name')
                dtype = inp.get('data_type') or inp.get('datatype')
                if name and dtype:
                    inputs_info.append((name, dtype))
            for out in outputs:
                name = out.get('name')
                if name:
                    outputs_names.append(name)
        else:
            # gRPC protobuf message with .input/.output
            inputs = getattr(cfg, 'input', []) or []
            outputs = getattr(cfg, 'output', []) or []
            for inp in inputs:
                name = getattr(inp, 'name', None)
                dtype = getattr(inp, 'data_type', None) or getattr(
                    inp, 'datatype', None)
                if name and dtype:
                    inputs_info.append((name, dtype))
            for out in outputs:
                name = getattr(out, 'name', None)
                if name:
                    outputs_names.append(name)

        return inputs_info, outputs_names

    def _load_model_info(self) -> None:
        # Try metadata first
        inputs_info: List[Tuple[str, str]] = []
        outputs_names: List[str] = []

        try:
            meta = self.triton_client.get_model_metadata(self.endpoint)
            ii, on = self._extract_io_from_metadata(meta)
            inputs_info.extend(ii)
            outputs_names.extend(on)
        except Exception:
            pass

        # Fallback to config if needed
        if not inputs_info or not outputs_names:
            try:
                cfg = self.triton_client.get_model_config(self.endpoint)
                ii, on = self._extract_io_from_config(cfg)
                if not inputs_info:
                    inputs_info = ii
                if not outputs_names:
                    outputs_names = on
            except Exception:
                pass

        # Populate attributes
        if inputs_info:
            self.input_names = [n for n, _ in inputs_info]
            self.input_formats = [dt for _, dt in inputs_info]
            # Convert Triton dtypes to numpy
            np_types: List[type] = []
            for dt in self.input_formats:
                try:
                    np_dtype = triton_to_numpy_dtype(dt)  # returns np.dtype
                    np_types.append(np_dtype.type if hasattr(
                        np_dtype, 'type') else np_dtype)
                except Exception:
                    # Unknown type; default to np.float32
                    np_types.append(np.float32)
            self.np_input_formats = np_types
        if outputs_names:
            self.output_names = outputs_names

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        '''
        Call the model with the given inputs.
        Args:
            *inputs (List[np.ndarray]): Input data to the model.
        Returns:
            (List[np.ndarray]): Model outputs.
        '''
        if not self.endpoint:
            raise ValueError("Model endpoint is not specified.")

        # Ensure model info is loaded
        if not self.input_names or not self.output_names:
            try:
                self._load_model_info()
            except Exception:
                pass

        # If we know number of inputs, validate
        if self.input_names and len(inputs) != len(self.input_names):
            raise ValueError(
                f"Expected {len(self.input_names)} inputs, got {len(inputs)}.")

        infer_inputs = []
        for idx, arr in enumerate(inputs):
            if not isinstance(arr, np.ndarray):
                arr = np.asarray(arr)
            # Cast to expected dtype if known
            if self.np_input_formats and idx < len(self.np_input_formats):
                try:
                    arr = arr.astype(self.np_input_formats[idx], copy=False)
                except Exception:
                    pass
            name = self.input_names[idx] if self.input_names and idx < len(
                self.input_names) else f'INPUT{idx}'
            dtype_str = np_to_triton_dtype(arr.dtype)
            inp = self.InferInput(name, arr.shape, dtype_str)
            inp.set_data_from_numpy(arr)
            infer_inputs.append(inp)

        infer_outputs = None
        if self.output_names:
            infer_outputs = [self.InferRequestedOutput(
                name) for name in self.output_names]

        result = self.triton_client.infer(
            self.endpoint, inputs=infer_inputs, outputs=infer_outputs)

        # If output names unknown, try to discover from response
        if not self.output_names:
            try:
                resp = result.get_response()
                if isinstance(resp, dict):
                    self.output_names = [o['name']
                                         for o in resp.get('outputs', [])]
                elif hasattr(resp, 'outputs'):
                    self.output_names = [
                        o.name for o in getattr(resp, 'outputs')]
            except Exception:
                pass

        outputs: List[np.ndarray] = []
        if self.output_names:
            for name in self.output_names:
                outputs.append(result.as_numpy(name))
        else:
            # As a last resort, attempt common default names
            # This is unlikely but provides a minimal fallback.
            try_names = ['OUTPUT0', 'output__0', 'output0']
            gathered = False
            for n in try_names:
                try:
                    out = result.as_numpy(n)
                    if out is not None:
                        outputs.append(out)
                        gathered = True
                except Exception:
                    continue
            if not gathered:
                raise RuntimeError(
                    "Could not determine output names from Triton response.")
        return outputs
