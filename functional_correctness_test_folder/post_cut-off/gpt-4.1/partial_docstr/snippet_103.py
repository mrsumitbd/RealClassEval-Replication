
import numpy as np
from typing import List


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
        import tritonclient.http as httpclient
        import tritonclient.grpc as grpcclient

        self.url = url
        self.endpoint = endpoint
        self.scheme = scheme.lower() if scheme else 'http'

        if self.scheme == 'grpc':
            self.triton_client = grpcclient.InferenceServerClient(url=self.url)
            self.InferInput = grpcclient.InferInput
            self.InferRequestedOutput = grpcclient.InferRequestedOutput
        else:
            self.triton_client = httpclient.InferenceServerClient(url=self.url)
            self.InferInput = httpclient.InferInput
            self.InferRequestedOutput = httpclient.InferRequestedOutput

        # Get model metadata
        if self.scheme == 'grpc':
            metadata = self.triton_client.get_model_metadata(self.endpoint)
            config = self.triton_client.get_model_config(self.endpoint)
        else:
            metadata = self.triton_client.get_model_metadata(self.endpoint)
            config = self.triton_client.get_model_config(self.endpoint)

        self.input_names = [inp['name'] for inp in metadata['inputs']]
        self.output_names = [out['name'] for out in metadata['outputs']]
        self.input_formats = [inp['datatype'] for inp in metadata['inputs']]
        self.np_input_formats = [self._triton_dtype_to_np(
            dt) for dt in self.input_formats]

    def _triton_dtype_to_np(self, dtype: str):
        # Triton datatypes to numpy types
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
            'BYTES': np.object_
        }
        return mapping.get(dtype, np.float32)

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        infer_inputs = []
        for i, (inp, name, dtype) in enumerate(zip(inputs, self.input_names, self.input_formats)):
            infer_input = self.InferInput(name, inp.shape, dtype)
            infer_input.set_data_from_numpy(inp)
            infer_inputs.append(infer_input)

        outputs = [self.InferRequestedOutput(
            name) for name in self.output_names]

        if self.scheme == 'grpc':
            results = self.triton_client.infer(
                self.endpoint, infer_inputs, outputs=outputs)
            return [results.as_numpy(name) for name in self.output_names]
        else:
            results = self.triton_client.infer(
                self.endpoint, infer_inputs=infer_inputs, outputs=outputs)
            return [results.as_numpy(name) for name in self.output_names]
