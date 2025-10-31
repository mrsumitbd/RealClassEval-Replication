import numpy as np
from typing import List, Optional


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
        from urllib.parse import urlparse
        self.endpoint: str = endpoint
        self.url: str = url
        self.triton_client = None
        self.InferInput = None
        self.InferRequestedOutput = None
        self.input_formats: List[str] = []
        self.np_input_formats: List[np.dtype] = []
        self.input_names: List[str] = []
        self.output_names: List[str] = []

        parsed = urlparse(
            url if '://' in url else f'{scheme or "http"}://{url}')
        resolved_scheme = scheme.lower() if scheme else (
            parsed.scheme.lower() if parsed.scheme else 'http')
        hostport = parsed.netloc if parsed.netloc else parsed.path

        if resolved_scheme == 'grpc':
            import tritonclient.grpc as grpcclient
            from tritonclient.utils import triton_to_np_dtype
            self.triton_client = grpcclient.InferenceServerClient(hostport)
            self.InferInput = grpcclient.InferInput
            self.InferRequestedOutput = grpcclient.InferRequestedOutput
            # Prefer JSON to unify handling
            try:
                meta = self.triton_client.get_model_metadata(
                    self.endpoint, as_json=True)
            except TypeError:
                # Older clients: return object
                meta_obj = self.triton_client.get_model_metadata(self.endpoint)
                meta = {
                    'inputs': [{'name': i.name, 'datatype': i.datatype, 'shape': list(i.shape)} for i in meta_obj.inputs],
                    'outputs': [{'name': o.name, 'datatype': o.datatype, 'shape': list(o.shape)} for o in meta_obj.outputs],
                }
            self.input_names = [i['name'] for i in meta.get('inputs', [])]
            self.output_names = [o['name'] for o in meta.get('outputs', [])]
            self.input_formats = [i['datatype']
                                  for i in meta.get('inputs', [])]
            self.np_input_formats = [triton_to_np_dtype(
                dt) for dt in self.input_formats]
        else:
            import tritonclient.http as httpclient
            from tritonclient.utils import triton_to_np_dtype
            self.triton_client = httpclient.InferenceServerClient(hostport)
            self.InferInput = httpclient.InferInput
            self.InferRequestedOutput = httpclient.InferRequestedOutput
            meta = self.triton_client.get_model_metadata(self.endpoint)
            self.input_names = [i['name'] for i in meta.get('inputs', [])]
            self.output_names = [o['name'] for o in meta.get('outputs', [])]
            self.input_formats = [i['datatype']
                                  for i in meta.get('inputs', [])]
            self.np_input_formats = [triton_to_np_dtype(
                dt) for dt in self.input_formats]

        if not self.endpoint:
            raise ValueError("endpoint (model name) must be provided.")
        if not self.input_names:
            raise RuntimeError(
                "Failed to fetch model inputs from Triton server.")
        if not self.output_names:
            raise RuntimeError(
                "Failed to fetch model outputs from Triton server.")

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        if len(inputs) != len(self.input_names):
            raise ValueError(
                f"Expected {len(self.input_names)} inputs but got {len(inputs)}.")

        triton_inputs = []
        for idx, (name, triton_dtype, expected_np_dtype, arr) in enumerate(
            zip(self.input_names, self.input_formats,
                self.np_input_formats, inputs)
        ):
            if not isinstance(arr, np.ndarray):
                arr = np.asarray(arr)

            # Handle BYTES specially; do not force-cast to numeric dtype
            if triton_dtype == 'BYTES':
                arr = self._ensure_bytes_object_array(arr)
            else:
                # Cast to expected dtype if needed
                if expected_np_dtype is not None and arr.dtype != expected_np_dtype:
                    try:
                        arr = arr.astype(expected_np_dtype, copy=False)
                    except Exception as e:
                        raise TypeError(
                            f"Input {idx} ('{name}') cannot be cast to required dtype {expected_np_dtype}: {e}")

            infer_inp = self.InferInput(name, arr.shape, triton_dtype)
            infer_inp.set_data_from_numpy(arr)
            triton_inputs.append(infer_inp)

        requested_outputs = [self.InferRequestedOutput(
            name) for name in self.output_names]
        results = self.triton_client.infer(
            self.endpoint, inputs=triton_inputs, outputs=requested_outputs)

        outputs: List[np.ndarray] = []
        # HTTP and gRPC responses both support as_numpy(name)
        for name in self.output_names:
            out = results.as_numpy(name)
            outputs.append(out)
        return outputs

    @staticmethod
    def _ensure_bytes_object_array(arr: np.ndarray) -> np.ndarray:
        if arr.dtype == object:
            # Ensure all elements are bytes
            flat = arr.ravel()
            for i in range(flat.size):
                v = flat[i]
                if isinstance(v, str):
                    flat[i] = v.encode('utf-8')
                elif isinstance(v, (bytes, bytearray, memoryview)):
                    flat[i] = bytes(v)
                else:
                    flat[i] = str(v).encode('utf-8')
            return arr
        if np.issubdtype(arr.dtype, np.bytes_):
            return arr.astype(object)
        if np.issubdtype(arr.dtype, np.str_):
            return np.vectorize(lambda x: x.encode('utf-8'), otypes=[object])(arr)
        # Fallback: convert to string then encode
        return np.vectorize(lambda x: str(x).encode('utf-8'), otypes=[object])(arr)
