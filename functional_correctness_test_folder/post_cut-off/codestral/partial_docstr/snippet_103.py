
import numpy as np
from typing import List
from tritonclient.utils import InferenceServerException
from tritonclient.grpc import InferenceServerClient, InferInput, InferRequestedOutput
from tritonclient.http import InferenceServerClient as HTTPInferenceServerClient, InferInput as HTTPInferInput, InferRequestedOutput as HTTPInferRequestedOutput


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
        if scheme == 'grpc':
            self.triton_client = InferenceServerClient(url=url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput
        else:
            self.triton_client = HTTPInferenceServerClient(url=url)
            self.InferInput = HTTPInferInput
            self.InferRequestedOutput = HTTPInferRequestedOutput

        model_metadata = self.triton_client.get_model_metadata(
            model_name=endpoint)
        self.input_names = [input['name'] for input in model_metadata.inputs]
        self.output_names = [output['name']
                             for output in model_metadata.outputs]
        self.input_formats = [input['datatype']
                              for input in model_metadata.inputs]
        self.np_input_formats = [np.float32 if format == 'FP32' else np.int32 if format ==
                                 'INT32' else np.int8 for format in self.input_formats]

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        inputs = [input.astype(format) for input, format in zip(
            inputs, self.np_input_formats)]
        infer_inputs = [self.InferInput(name, input.shape, format) for name, input, format in zip(
            self.input_names, inputs, self.input_formats)]
        for infer_input, input in zip(infer_inputs, inputs):
            infer_input.set_data_from_numpy(input)

        infer_outputs = [self.InferRequestedOutput(
            name) for name in self.output_names]
        response = self.triton_client.infer(
            model_name=self.endpoint, inputs=infer_inputs, outputs=infer_outputs)
        return [response.as_numpy(name) for name in self.output_names]
