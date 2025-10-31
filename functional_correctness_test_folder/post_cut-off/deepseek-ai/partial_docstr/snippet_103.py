
import numpy as np
from typing import List
import tritonclient.http as httpclient
import tritonclient.grpc as grpcclient
from tritonclient.utils import np_to_triton_dtype


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
        self.url = url
        self.endpoint = endpoint
        self.scheme = scheme.lower() if scheme else 'http'

        if self.scheme == 'http':
            self.triton_client = httpclient.InferenceServerClient(url=url)
            self.InferInput = httpclient.InferInput
            self.InferRequestedOutput = httpclient.InferRequestedOutput
        elif self.scheme == 'grpc':
            self.triton_client = grpcclient.InferenceServerClient(url=url)
            self.InferInput = grpcclient.InferInput
            self.InferRequestedOutput = grpcclient.InferRequestedOutput
        else:
            raise ValueError(
                f"Unsupported scheme: {scheme}. Use 'http' or 'grpc'.")

        model_metadata = self.triton_client.get_model_metadata(endpoint)
        self.input_names = [input['name']
                            for input in model_metadata['inputs']]
        self.output_names = [output['name']
                             for output in model_metadata['outputs']]
        self.input_formats = [input['datatype']
                              for input in model_metadata['inputs']]
        self.np_input_formats = []
        for fmt in self.input_formats:
            if fmt == 'FP32':
                self.np_input_formats.append(np.float32)
            elif fmt == 'FP64':
                self.np_input_formats.append(np.float64)
            elif fmt == 'INT32':
                self.np_input_formats.append(np.int32)
            elif fmt == 'INT64':
                self.np_input_formats.append(np.int64)
            else:
                raise ValueError(f"Unsupported data type: {fmt}")

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        if len(inputs) != len(self.input_names):
            raise ValueError(
                f"Expected {len(self.input_names)} inputs, got {len(inputs)}")

        triton_inputs = []
        for i, (input_data, input_name, np_fmt) in enumerate(zip(inputs, self.input_names, self.np_input_formats)):
            if input_data.dtype != np_fmt:
                input_data = input_data.astype(np_fmt)
            triton_input = self.InferInput(
                input_name, input_data.shape, np_to_triton_dtype(np_fmt))
            triton_input.set_data_from_numpy(input_data)
            triton_inputs.append(triton_input)

        outputs = [self.InferRequestedOutput(
            output_name) for output_name in self.output_names]

        response = self.triton_client.infer(
            model_name=self.endpoint,
            inputs=triton_inputs,
            outputs=outputs
        )

        return [response.as_numpy(output_name) for output_name in self.output_names]
