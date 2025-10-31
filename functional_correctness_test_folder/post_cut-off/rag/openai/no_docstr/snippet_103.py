
import json
import re
import urllib.parse
from typing import List, Optional

import numpy as np
from tritonclient import http, grpc, utils

# Mapping from Triton datatype to numpy dtype
_TRITON_TO_NP = {
    "FP32": np.float32,
    "FP64": np.float64,
    "INT32": np.int32,
    "INT64": np.int64,
    "UINT32": np.uint32,
    "UINT64": np.uint64,
    "INT8": np.int8,
    "INT16": np.int16,
    "UINT8": np.uint8,
    "UINT16": np.uint16,
    "BOOL": np.bool_,
    "BYTES": np.object_,
    "UINT8": np.uint8,
    "UINT16": np.uint16,
    "UINT32": np.uint32,
    "UINT64": np.uint64,
    "INT8": np.int8,
    "INT16": np.int16,
    "INT32": np.int32,
    "INT64": np.int64,
    "FP16": np.float16,
    "BF16": np.float16,
    "FP64": np.float64,
    "STRING": np.object_,
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
        # Determine scheme
        if not scheme:
            scheme = parsed.scheme or "http"
        scheme = scheme.lower()
        if scheme not in ("http", "grpc"):
            raise ValueError(
                f"Unsupported scheme '{scheme}'. Only 'http' and 'grpc' are supported.")
        # Determine endpoint
        if not endpoint:
            # Path may be /<endpoint>/<task_name> or /<endpoint>
            path_parts = [p for p in parsed.path.split("/") if p]
            if not path_parts:
                raise ValueError(
                    "Endpoint not specified and could not be inferred from URL path.")
            endpoint = path_parts[0]
        # Base URL (scheme://netloc)
        self.url = f"{scheme}://{parsed.netloc}"
        self.endpoint = endpoint
        self.scheme = scheme

        # Create the Triton client
        if scheme == "http":
            self.triton_client = http.InferenceServerClient(
                url=self.url, verbose=False)
            self.InferInput = http.InferInput
            self.InferRequestedOutput = http.InferRequestedOutput
        else:  # grpc
            self.triton_client = grpc.InferenceServerClient(
                url=self.url, verbose=False)
            self.InferInput = grpc.InferInput
            self.InferRequestedOutput = grpc.InferRequestedOutput

        # Retrieve model metadata
        try:
            metadata = self.triton_client.get_model_metadata(self.endpoint)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to get metadata for model '{self.endpoint}': {exc}") from exc

        # Parse input and output information
        self.input_names = [inp["name"] for inp in metadata["inputs"]]
        self.input_formats = [inp["datatype"] for inp in metadata["inputs"]]
        self.np_input_formats = [
            _TRITON_TO_NP.get(dt, np.object_) for dt in self.input_formats
        ]
        self.output_names = [out["name"] for out in metadata["outputs"]]

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
                f"Expected {len(self.input_names)} inputs, got {len(inputs)}."
            )

        # Build InferInput objects
        infer_inputs = []
        for name, inp, dtype, shape in zip(
            self.input_names, inputs, self.input_formats, [
                i.shape for i in inputs]
        ):
            infer_input = self.InferInput(name,
