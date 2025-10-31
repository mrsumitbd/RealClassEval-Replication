from typing import List, Optional, Any
import numpy as np
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
        try:
            from tritonclient import http as httpclient
        except Exception:
            httpclient = None
        try:
            from tritonclient import grpc as grpcclient
        except Exception:
            grpcclient = None
        try:
            from tritonclient.utils import np_to_triton_dtype, triton_to_np_dtype
        except Exception as e:
            raise ImportError(
                "tritonclient is required to use TritonRemoteModel") from e

        original_url = url
        parsed = urlparse(url) if '://' in url else None

        netloc = ''
        if parsed:
            if not scheme and parsed.scheme:
                scheme = parsed.scheme
            netloc = parsed.netloc
            if not endpoint:
                path_parts = [p for p in parsed.path.split('/') if p]
                if path_parts:
                    endpoint = path_parts[0]
        else:
            # url might be "host:port" or "host:port/endpoint"
            if '/' in url:
                netloc, rest = url.split('/', 1)
                if not endpoint and rest:
                    endpoint = rest.split('/', 1)[0]
            else:
                netloc = url

        if not netloc:
            # If user passed separate args, url could be just "host:port"
            netloc = original_url

        if not scheme:
            scheme = 'http'
        scheme = scheme.lower()

        if not endpoint:
            raise ValueError(
                "Endpoint (model name) could not be determined. Please provide endpoint or use a URL with /<endpoint>.")

        self.endpoint: str = endpoint
        self.url: str = f"{scheme}://{netloc}"

        # Select client based on scheme
        if scheme in ('grpc', 'grpcs'):
            if grpcclient is None:
                raise ImportError(
                    "tritonclient[grpc] is required for gRPC scheme")
            self.triton_client = grpcclient.InferenceServerClient(url=netloc)
            self.InferInput = grpcclient.InferInput
            self.InferRequestedOutput = grpcclient.InferRequestedOutput
        else:
            if httpclient is None:
                raise ImportError(
                    "tritonclient[http] is required for HTTP scheme")
            # http client supports scheme parameter ('http'/'https')
            http_scheme = 'https' if scheme == 'https' else 'http'
            self.triton_client = httpclient.InferenceServerClient(
                url=netloc, scheme=http_scheme)
            self.InferInput = httpclient.InferInput
            self.InferRequestedOutput = httpclient.InferRequestedOutput

        # Introspect model metadata/config
        self.input_names: List[str] = []
        self.output_names: List[str] = []
        self.input_formats: List[str] = []
        self.np_input_formats: List[Any] = []
        self.input_shapes: List[List[int]] = []

        def _extract_from_metadata(meta: Any) -> None:
            inputs = []
            outputs = []
            if isinstance(meta, dict):
                inputs = meta.get('inputs', meta.get('input', [])) or []
                outputs = meta.get('outputs', meta.get('output', [])) or []
                for i in inputs:
                    name = i.get('name')
                    dtype = i.get('datatype') or i.get('data_type')
                    shape = i.get('shape') or i.get('dims')
                    if name:
                        self.input_names.append(name)
                        if dtype:
                            self.input_formats.append(dtype)
                            try:
                                self.np_input_formats.append(
                                    triton_to_np_dtype(dtype))
                            except Exception:
                                self.np_input_formats.append(np.float32)
                        if shape is not None:
                            self.input_shapes.append(list(shape))
                for o in outputs:
                    name = o.get('name')
                    if name:
                        self.output_names.append(name)
            else:
                # Assume gRPC protobuf responses
                ins = getattr(meta, 'inputs', None)
                outs = getattr(meta, 'outputs', None)
                if ins:
                    for i in ins:
                        name = getattr(i, 'name', None)
                        dtype = getattr(
                            i, 'datatype', getattr(i, 'data_type', None))
                        shape = getattr(i, 'shape', getattr(i, 'dims', None))
                        if name:
                            self.input_names.append(name)
                            if dtype:
                                self.input_formats.append(dtype)
                                try:
                                    self.np_input_formats.append(
                                        triton_to_np_dtype(dtype))
                                except Exception:
                                    self.np_input_formats.append(np.float32)
                            if shape is not None:
                                try:
                                    self.input_shapes.append(list(shape))
                                except Exception:
                                    pass
                if outs:
                    for o in outs:
                        name = getattr(o, 'name', None)
                        if name:
                            self.output_names.append(name)

        # Try metadata first
        try:
            meta = self.triton_client.get_model_metadata(self.endpoint)
            _extract_from_metadata(meta)
        except Exception:
            pass

        # Fallback to model config for shapes or names if missing
        need_shapes = len(self.input_shapes) != len(self.input_names)
        need_outputs = len(self.output_names) == 0
        if need_shapes or need_outputs or len(self.input_names) == 0:
            try:
                cfg = self.triton_client.get_model_config(self.endpoint)
                if isinstance(cfg, dict):
                    cfg = cfg.get('config', cfg)
                    inputs = cfg.get('input', [])
                    outputs = cfg.get('output', [])
                    if need_shapes:
                        name_to_shape = {i.get('name'): i.get(
                            'dims') for i in inputs if i.get('name') is not None}
                        self.input_shapes = [
                            list(name_to_shape.get(n, [])) for n in self.input_names]
                    if len(self.input_names) == 0 and inputs:
                        self.input_names = [
                            i.get('name') for i in inputs if i.get('name') is not None]
                        if need_shapes:
                            self.input_shapes = [
                                list((i.get('dims') or [])) for i in inputs]
                    if need_outputs and outputs:
                        self.output_names = [
                            o.get('name') for o in outputs if o.get('name') is not None]
                else:
                    config = getattr(cfg, 'config', cfg)
                    inputs = getattr(config, 'input', []) or []
                    outputs = getattr(config, 'output', []) or []
                    if len(self.input_names) == 0 and inputs:
                        self.input_names = [getattr(i, 'name', None) for i in inputs if getattr(
                            i, 'name', None) is not None]
                    if need_shapes:
                        name_to_shape = {}
                        for i in inputs:
                            nm = getattr(i, 'name', None)
                            dm = getattr(i, 'dims', None)
                            if nm is not None and dm is not None:
                                name_to_shape[nm] = list(dm)
                        if self.input_names:
                            self.input_shapes = [name_to_shape.get(
                                n, []) for n in self.input_names]
                    if need_outputs and outputs:
                        self.output_names = [getattr(o, 'name', None) for o in outputs if getattr(
                            o, 'name', None) is not None]
            except Exception:
                pass

        # Default np dtypes if not resolved
        if len(self.np_input_formats) != len(self.input_names):
            # Try to infer from shapes list size
            for _ in range(len(self.input_names) - len(self.np_input_formats)):
                self.np_input_formats.append(np.float32)

        self._np_to_triton_dtype = np_to_triton_dtype

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        '''
        Call the model with the given inputs.
        Args:
            *inputs (List[np.ndarray]): Input data to the model.
        Returns:
            (List[np.ndarray]): Model outputs.
        '''
        if not inputs:
            raise ValueError("At least one input is required")
        if self.input_names and len(inputs) != len(self.input_names):
            raise ValueError(
                f"Model expects {len(self.input_names)} inputs, received {len(inputs)}")

        triton_inputs = []
        for idx, arr in enumerate(inputs):
            if not isinstance(arr, np.ndarray):
                arr = np.asarray(arr)
            # Cast dtype if known
            if idx < len(self.np_input_formats):
                target_dtype = np.dtype(self.np_input_formats[idx])
                if arr.dtype != target_dtype:
                    arr = arr.astype(target_dtype, copy=False)
            name = self.input_names[idx] if idx < len(
                self.input_names) else f"INPUT{idx}"
            infer_in = self.InferInput(name, list(
                arr.shape), self._np_to_triton_dtype(arr.dtype))
            infer_in.set_data_from_numpy(arr)
            triton_inputs.append(infer_in)

        triton_outputs = []
        for name in (self.output_names or []):
            triton_outputs.append(self.InferRequestedOutput(name))

        result = self.triton_client.infer(
            self.endpoint, inputs=triton_inputs, outputs=triton_outputs if triton_outputs else None)

        outputs: List[np.ndarray] = []
        names = self.output_names
        if not names:
            # Best-effort: some clients expose get_output_names(); fall back empty list
            get_names = getattr(result, "get_output_names", None)
            if callable(get_names):
                try:
                    names = list(get_names())
                except Exception:
                    names = []
        for name in names:
            outputs.append(result.as_numpy(name))
        return outputs
