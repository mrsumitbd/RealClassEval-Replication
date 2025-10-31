
import numpy as np
from typing import List
from tritonclient.utils import InferenceServerException
from tritonclient.grpc import InferenceServerClient as GrpcClient, InferInput, InferRequestedOutput
from tritonclient.http import InferenceServerClient as HttpClient


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
        if url:
            from urllib.parse import urlparse
            parsed_url = urlparse(url)
            if not scheme:
                scheme = parsed_url.scheme
            if not endpoint:
                endpoint = parsed_url.path.strip('/')
            url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        if scheme == 'grpc':
            self.triton_client = GrpcClient(url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput
        else:
            self.triton_client = HttpClient(url)
            self.InferInput = InferInput
            self.InferRequestedOutput = InferRequestedOutput

        self.endpoint = endpoint
        self.url = url

        model_metadata = self.triton_client.get_model_metadata(endpoint)
        self.input_names = [input.name for input in model_metadata.inputs]
        self.output_names = [output.name for output in model_metadata.outputs]
        self.input_formats = [
            input.datatype for input in model_metadata.inputs]
        self.np_input_formats = [np.dtype(input.datatype)
                                 for input in model_metadata.inputs]

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
        for i, (input_name, input_format, np_input_format, input_data) in enumerate(zip(self.input_names, self.input_formats, self.np_input_formats, inputs)):
            if input_data.dtype != np_input_format:
                input_data = input_data.astype(np_input_format)
            infer_input = self.InferInput(
                input_name, input_data.shape, input_format)
            infer_input.set_data_from_numpy(input_data)
            infer_inputs.append(infer_input)

        infer_outputs = [self.InferRequestedOutput(
            output_name) for output_name in self.output_names]

        try:
            response = self.triton_client.infer(
                self.endpoint, infer_inputs, outputs=infer_outputs)
        except InferenceServerException as e:
            raise RuntimeError(f"Inference failed: {e}")

        outputs = [response.as_numpy(output_name)
                   for output_name in self.output_names]
        return outputs
