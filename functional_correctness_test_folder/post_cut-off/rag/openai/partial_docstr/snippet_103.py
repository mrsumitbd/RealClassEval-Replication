
import json
import re
import urllib.parse
from typing import List, Optional

import numpy as np
from tritonclient.grpc import InferenceServerClient as GrpcClient
from tritonclient.http import InferenceServerClient as HttpClient
from tritonclient.grpc import InferInput as GrpcInferInput
from tritonclient.http import InferInput as HttpInferInput
from tritonclient.grpc import InferRequestedOutput as GrpcInferRequestedOutput
from tritonclient.http import InferRequestedOutput as HttpInferRequestedOutput


# Mapping from Triton datatype strings to numpy dtypes
_TRITON_TO_NUMPY = {
    "INT8": np.int8,
    "INT16": np.int16,
    "INT32": np.int32,
    "INT64": np.int64,
    "UINT8": np.uint8,
    "UINT16": np.uint16,
    "UINT32": np.uint32,
    "UINT64": np.uint64,
    "FP16": np.float16,
    "FP32": np.float32,
    "FP64": np.float64,
    "BOOL": np.bool_,
    "BYTES": np.object_,
}


class TritonRemoteModel:
    """
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
    """

    def __init__(self, url: str, endpoint: str = "", scheme: str = ""):
        """
        Initialize the TritonRemoteModel.
        Arguments may be provided individually or parsed from a collective 'url' argument of the form
            <scheme>://<netloc>/<endpoint>/<task_name>
        Args:
            url (str): The URL of the Triton server.
            endpoint (str): The name of the model on the Triton server.
            scheme (str): The communication scheme ('http' or 'grpc').
        """
        # Parse the URL
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme:
            raise ValueError(f"URL must include scheme: {url}")

        # Determine scheme
        if scheme:
            scheme = scheme.lower()
        else:
            scheme = parsed.scheme.lower()

        # Determine endpoint
        if endpoint:
            self.endpoint = endpoint
        else:
            # Path may be /<endpoint>/<task_name>
            path_parts = [p for p in parsed.path.split("/") if p]
            if not path_parts:
                raise ValueError(
                    f"Endpoint not provided and could not be inferred from URL: {url}")
            self.endpoint = path_parts[0]

        # Base URL (without endpoint)
        self.url = f"{parsed.scheme}://{parsed.netloc}"

        # Create the Triton client
        if scheme in ("http", "https"):
            self.triton_client = HttpClient(self.url, verbose=False)
            self.InferInput = HttpInferInput
            self.InferRequestedOutput = HttpInferRequestedOutput
        elif scheme == "grpc":
            self.triton_client = GrpcClient(self.url, verbose=False)
            self.InferInput = GrpcInferInput
            self.InferRequestedOutput = GrpcInferRequestedOutput
        else:
            raise ValueError(
                f"Unsupported scheme '{scheme}'. Use 'http', 'https', or 'grpc'.")

        # Retrieve model metadata
        try:
            metadata = self.triton_client.get_model_metadata(self.endpoint)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to get metadata for model '{self.endpoint}': {exc}") from exc

        # Input names and formats
        self.input_names = [inp.name for inp in metadata.inputs]
        self.input_formats = [inp.datatype for inp in metadata.inputs]
        self.np_input_formats = [
            _TRITON_TO_NUMPY.get(dt, np.object_) for dt in self.input_formats
        ]

        # Output names
        self.output_names = [out.name for out in metadata.outputs]

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        """
        Call the model with the given inputs.
        Args:
            *inputs (List[np.ndarray]): Input data to the model.
        Returns:
            (List[np.ndarray]): Model outputs.
        """
        if len(inputs) != len(self.input_names):
            raise ValueError(
                f"Expected {len(self.input_names)} inputs, got {len(inputs)}"
            )

        # Build InferInput objects
        triton_inputs = []
        for name, array, dtype in zip(self.input_names, inputs, self.input_formats):
            inp = self.InferInput(name, array.shape, dtype)
            inp.set_data_from_numpy(array)
            triton_inputs.append(inp)

        # Build InferRequestedOutput objects
        triton_outputs = [self.InferRequestedOutput(
            name) for name in self.output_names]

        # Perform inference
        try:
            response = self.triton_client.infer(
                self.endpoint, inputs=
