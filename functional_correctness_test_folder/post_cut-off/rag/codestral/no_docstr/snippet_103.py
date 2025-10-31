
import numpy as np
from typing import List, Optional, Union
from tritonclient.http import InferenceServerClient as HTTPClient, InferInput, InferRequestedOutput
from tritonclient.grpc import InferenceServerClient as GRPCClient


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
        if scheme:
            self.url = f"{scheme}://{url}"
        else:
            self.url = url

        if endpoint:
            self.endpoint = endpoint
        else:
            self.endpoint = self.url.split('/')[-1]

        if 'http' in self.url:
            self.triton_client = HTTPClient(url=self.url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput
        elif 'grpc' in self.url:
            self.triton_client = GRPCClient(url=self.url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput
        else:
            raise ValueError("Invalid scheme. Must be 'http' or 'grpc'.")

        model_metadata = self.triton_client.get_model_metadata(
            model_name=self.endpoint)
        self.input_formats = [input['datatype']
                              for input in model_metadata.inputs]
        self.np_input_formats = [np.dtype(format)
                                 for format in self.input_formats]
        self.input_names = [input['name'] for input in model_metadata.inputs]
        self.output_names = [output['name']
                             for output in model_metadata.outputs]

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
                f"Expected {len(self.input_names)} inputs, got {len(inputs)}")

        infer_inputs = []
        for i, (input_name, input_data) in enumerate(zip(self.input_names, inputs)):
            infer_input = self.InferInput(
                input_name, input_data.shape, self.input_formats[i])
            infer_input.set_data_from_numpy(input_data)
            infer_inputs.append(infer_input)

        infer_outputs = [self.InferRequestedOutput(
            output_name) for output_name in self.output_names]

        response = self.triton_client.infer(
            model_name=self.endpoint,
            inputs=infer_inputs,
            outputs=infer_outputs
        )

        return [response.as_numpy(output_name) for output_name in self.output_names]
