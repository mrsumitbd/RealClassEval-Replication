
import json
from typing import List
import numpy as np
import requests


class TritonRemoteModel:
    """
    A simple HTTP client for NVIDIA Triton Inference Server.
    """

    _DTYPE_MAP = {
        np.dtype('float32'): 'FP32',
        np.dtype('float64'): 'FP64',
        np.dtype('int32'): 'INT32',
        np.dtype('int64'): 'INT64',
        np.dtype('uint8'): 'UINT8',
        np.dtype('bool'): 'BOOL',
    }

    def __init__(self, url: str, endpoint: str = '', scheme: str = ''):
        """
        Parameters
        ----------
        url : str
            Base URL of the Triton server (e.g. "http://localhost:8000").
        endpoint : str, optional
            Triton inference endpoint (e.g. "v2/models/my_model/infer").
            If empty, the URL is used as-is.
        scheme : str, optional
            Communication scheme ('http' or 'grpc'). Only 'http' is supported.
        """
        if scheme and scheme.lower() != 'http':
            raise NotImplementedError(
                "Only HTTP scheme is supported in this implementation.")
        self.base_url = url.rstrip('/')
        self.endpoint = endpoint.lstrip('/') if endpoint else ''
        self.full_url = f"{self.base_url}/{self.endpoint}" if self.endpoint else self.base_url

    def _dtype_to_triton(self, dtype: np.dtype) -> str:
        if dtype in self._DTYPE_MAP:
            return self._DTYPE_MAP[dtype]
        raise ValueError(f"Unsupported dtype for Triton: {dtype}")

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        """
        Send inference request to Triton and return the outputs.

        Parameters
        ----------
        *inputs : np.ndarray
            One or more numpy arrays to be sent as inputs.

        Returns
        -------
        List[np.ndarray]
            List of numpy arrays returned by Triton.
        """
        if not inputs:
            raise ValueError("At least one input array must be provided.")

        # Build request payload
        request_inputs = []
        for idx, arr in enumerate(inputs):
            name = f"INPUT{idx}"
            request_inputs.append({
                "name": name,
                "shape": list(arr.shape),
                "datatype": self._dtype_to_triton(arr.dtype),
                "data": arr.tolist()
            })

        payload = {"inputs": request_inputs}

        # Send request
        try:
            resp = requests.post(self.full_url, json=payload, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError(
                f"Failed to communicate with Triton server: {e}") from e

        # Parse response
        try:
            resp_json = resp.json()
        except json.JSONDecodeError as e:
            raise RuntimeError(
                f"Invalid JSON response from Triton: {e}") from e

        if "outputs" not in resp_json:
            raise RuntimeError(
                "Response JSON does not contain 'outputs' field.")

        outputs = []
        for out in resp_json["outputs"]:
            data = out.get("data")
            if data is None:
                raise RuntimeError(
                    f"Output {out.get('name')} missing 'data' field.")
            dtype_str = out.get("datatype")
            if dtype_str is None:
                raise RuntimeError(
                    f"Output {out.get('name')} missing 'datatype' field.")
            # Map Triton datatype back to numpy dtype
            np_dtype = None
            for k, v in self._DTYPE_MAP.items():
                if v == dtype_str:
                    np_dtype = k
                    break
            if np_dtype is None:
                raise RuntimeError(f"Unsupported Triton datatype: {dtype_str}")

            arr = np.array(data, dtype=np_dtype)
            outputs.append(arr)

        return outputs
