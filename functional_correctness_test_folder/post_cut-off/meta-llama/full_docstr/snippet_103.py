
import numpy as np
from urllib.parse import urlparse
import tritonclient.http as httpclient
import tritonclient.grpc as grpcclient
from tritonclient.utils import *


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
        if not endpoint or not scheme:
            parsed_url = urlparse(url)
            scheme = parsed_url.scheme
            endpoint = parsed_url.path.strip('/').split('/')[0]

        self.endpoint = endpoint
        self.url = url

        if scheme == 'http':
            self.triton_client = httpclient.InferenceServerClient(
                url=parsed_url.netloc, verbose=False)
            self.InferInput = httpclient.InferInput
            self.InferRequestedOutput = httpclient.InferRequestedOutput
        elif scheme == 'grpc':
            self.triton_client = grpcclient.InferenceServerClient(
                url=parsed_url.netloc, verbose=False)
            self.InferInput = grpcclient.InferInput
            self.InferRequestedOutput = grpcclient.InferRequestedOutput
        else:
            raise ValueError(
                "Invalid scheme. Supported schemes are 'http' and 'grpc'.")

        model_metadata = self.triton_client.get_model_metadata(
            model_name=endpoint)
        model_config = self.triton_client.get_model_config(model_name=endpoint)

        self.input_names = [input.name for input in model_metadata.inputs]
        self.output_names = [output.name for output in model_metadata.outputs]
        self.input_formats = [
            input.data_type for input in model_config.config.input]
        self.np_input_formats = [self._triton_dtype_to_np(
            dtype) for dtype in self.input_formats]

    def _triton_dtype_to_np(self, dtype):
        dtype_map = {
            'TYPE_BOOL': np.bool_,
            'TYPE_UINT8': np.uint8,
            'TYPE_UINT16': np.uint16,
            'TYPE_UINT32': np.uint32,
            'TYPE_UINT64': np.uint64,
            'TYPE_INT8': np.int8,
            'TYPE_INT16': np.int16,
            'TYPE_INT32': np.int32,
            'TYPE_INT64': np.int64,
            'TYPE_FP16': np.float16,
            'TYPE_FP32': np.float32,
            'TYPE_FP64': np.float64,
            'TYPE_STRING': np.object_,
        }
        return dtype_map[dtype]

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        '''
        Call the model with the given inputs.
        Args:
            *inputs (List[np.ndarray]): Input data to the model.
        Returns:
            (List[np.ndarray]): Model outputs.
        '''
        inputs_dict = {name: data for name,
                       data in zip(self.input_names, inputs)}

        # Create input tensors
        input_tensors = []
        for name, data in inputs_dict.items():
            input_tensors.append(self.InferInput(
                name, data.shape, np_to_triton_dtype(data.dtype)))

        # Initialize the data for the input tensors
        for tensor, data in zip(input_tensors, inputs_dict.values()):
            tensor.set_data_from_numpy(data)

        # Create output tensors
        output_tensors = [self.InferRequestedOutput(
            name) for name in self.output_names]

        # Create the inference request
        response = self.triton_client.infer(
            model_name=self.endpoint, inputs=input_tensors, outputs=output_tensors)

        # Get the output tensors
        outputs = [response.as_numpy(name) for name in self.output_names]

        return outputs
