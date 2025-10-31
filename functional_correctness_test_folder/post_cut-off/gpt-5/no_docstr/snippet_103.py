from typing import List, Dict, Any
import numpy as np
import requests


class TritonRemoteModel:
    def __init__(self, url: str, endpoint: str = '', scheme: str = ''):
        if url.startswith('http://') or url.startswith('https://'):
            base = url.rstrip('/')
        else:
            sc = scheme if scheme else 'http'
            base = f'{sc}://{url}'.rstrip('/')

        if not endpoint:
            raise ValueError('endpoint (model name) must be provided')

        self._base_url = base
        self._model = endpoint.strip('/')

        self._session = requests.Session()
        self._np_to_triton = {
            np.bool_: 'BOOL',
            np.int8: 'INT8',
            np.int16: 'INT16',
            np.int32: 'INT32',
            np.int64: 'INT64',
            np.uint8: 'UINT8',
            np.uint16: 'UINT16',
            np.uint32: 'UINT32',
            np.uint64: 'UINT64',
            np.float16: 'FP16',
            np.float32: 'FP32',
            np.float64: 'FP64',
            getattr(np, 'bfloat16', np.float16): 'BF16' if hasattr(np, 'bfloat16') else 'FP16',
            np.object_: 'BYTES',
        }
        # reverse map: handle aliasing
        self._triton_to_np = {
            'BOOL': np.bool_,
            'INT8': np.int8,
            'INT16': np.int16,
            'INT32': np.int32,
            'INT64': np.int64,
            'UINT8': np.uint8,
            'UINT16': np.uint16,
            'UINT32': np.uint32,
            'UINT64': np.uint64,
            'FP16': np.float16,
            'FP32': np.float32,
            'FP64': np.float64,
            'BF16': getattr(np, 'bfloat16', np.float16),
            'BYTES': np.object_,
        }

        self._inputs_meta: List[Dict[str, Any]] = []
        self._outputs_meta: List[Dict[str, Any]] = []
        self._fetch_metadata()

    def _fetch_metadata(self) -> None:
        url = f'{self._base_url}/v2/models/{self._model}'
        resp = self._session.get(url, timeout=10)
        resp.raise_for_status()
        meta = resp.json()
        inputs = meta.get('inputs') or []
        outputs = meta.get('outputs') or []

        if not inputs:
            # try config endpoint as fallback
            cfg_resp = self._session.get(
                f'{self._base_url}/v2/models/{self._model}/config', timeout=10)
            cfg_resp.raise_for_status()
            cfg = cfg_resp.json()
            inputs = cfg.get('input', [])
            outputs = cfg.get('output', [])

            # normalize keys to v2 style
            for i in inputs:
                if 'data_type' in i and 'datatype' not in i:
                    i['datatype'] = i['data_type']
                if 'dims' in i and 'shape' not in i:
                    # Triton config dims exclude batch dim; keep as dims
                    i['shape'] = i['dims']
            for o in outputs:
                if 'data_type' in o and 'datatype' not in o:
                    o['datatype'] = o['data_type']
                if 'dims' in o and 'shape' not in o:
                    o['shape'] = o['dims']

        self._inputs_meta = inputs
        self._outputs_meta = outputs

    def _infer_url(self) -> str:
        return f'{self._base_url}/v2/models/{self._model}/infer'

    def _dtype_to_triton(self, arr: np.ndarray) -> str:
        dt = arr.dtype
        # handle bytes/object heuristics
        if dt == np.object_:
            return 'BYTES'
        for k, v in self._np_to_triton.items():
            if dt == np.dtype(k):
                return v
        # Fallback for string types as BYTES
        if dt.kind in ('S', 'U'):
            return 'BYTES'
        raise ValueError(f'Unsupported numpy dtype: {dt}')

    def _encode_bytes_list(self, arr: np.ndarray) -> List[str]:
        out = []
        # Ensure object or bytes-like
        flat = arr.ravel()
        for v in flat:
            if isinstance(v, bytes):
                out.append(v.decode('latin1'))
            elif isinstance(v, str):
                out.append(v)
            elif v is None:
                out.append('')
            else:
                out.append(str(v))
        return out

    def _prepare_input_obj(self, name: str, arr: np.ndarray) -> Dict[str, Any]:
        dt = self._dtype_to_triton(arr)
        shape = list(arr.shape)
        if dt == 'BYTES':
            data = self._encode_bytes_list(arr)
        else:
            data = arr.ravel().tolist()
        return {'name': name, 'shape': shape, 'datatype': dt, 'data': data}

    def __call__(self, *inputs: np.ndarray) -> List[np.ndarray]:
        if not self._inputs_meta:
            raise RuntimeError('Model input metadata is unavailable')

        if inputs and len(inputs) != len(self._inputs_meta):
            raise ValueError(
                f'Expected {len(self._inputs_meta)} inputs, got {len(inputs)}')

        if not inputs:
            raise ValueError('No inputs provided')

        payload_inputs = []
        for idx, arr in enumerate(inputs):
            if not isinstance(arr, np.ndarray):
                arr = np.asarray(arr)
            name = self._inputs_meta[idx].get('name', f'INPUT__{idx}')
            payload_inputs.append(self._prepare_input_obj(name, arr))

        outputs = [{'name': o.get('name', f'OUTPUT__{i}')}
                   for i, o in enumerate(self._outputs_meta or [])]

        req = {'inputs': payload_inputs}
        if outputs:
            req['outputs'] = outputs

        resp = self._session.post(self._infer_url(), json=req, timeout=60)
        resp.raise_for_status()
        out = resp.json().get('outputs', [])

        result: List[np.ndarray] = []
        for o in out:
            name = o.get('name', '')
            dtype = o.get('datatype')
            shape = o.get('shape', [])
            data = o.get('data', [])
            if dtype is None:
                raise RuntimeError(f'Output {name} missing datatype')
            np_dtype = self._triton_to_np.get(dtype)
            if np_dtype is None:
                raise ValueError(
                    f'Unsupported Triton dtype in output {name}: {dtype}')
            if dtype == 'BYTES':
                arr = np.array(data, dtype=np.object_)
                if shape:
                    arr = arr.reshape(shape)
                result.append(arr)
            else:
                arr = np.array(data, dtype=np_dtype)
                if shape:
                    arr = arr.reshape(shape)
                result.append(arr)

        return result
