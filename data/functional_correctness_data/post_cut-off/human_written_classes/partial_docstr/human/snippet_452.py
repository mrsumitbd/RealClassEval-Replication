import requests
from pydantic import BaseModel, TypeAdapter, ValidationError
from urllib.parse import urlparse, urlunparse
from pydantic_core import InitErrorDetails

class HTTPClient:
    """HTTP Client for Tesseracts."""

    def __init__(self, url: str) -> None:
        self._url = self._sanitize_url(url)

    @staticmethod
    def _sanitize_url(url: str) -> str:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = f'http://{url}'
            parsed = urlparse(url)
        sanitized = urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))
        sanitized = sanitized.rstrip('/')
        return sanitized

    @property
    def url(self) -> str:
        """(Sanitized) URL to connect to."""
        return self._url

    def _request(self, endpoint: str, method: str='GET', payload: dict | None=None, run_id: str | None=None) -> dict:
        url = f"{self.url}/{endpoint.lstrip('/')}"
        if payload:
            encoded_payload = _tree_map(_encode_array, payload, is_leaf=lambda x: hasattr(x, 'shape'))
        else:
            encoded_payload = None
        params = {'run_id': run_id} if run_id is not None else {}
        response = requests.request(method=method, url=url, json=encoded_payload, params=params)
        if response.status_code == requests.codes.unprocessable_entity:
            try:
                data = response.json()
            except requests.JSONDecodeError:
                data = {}
            if 'detail' in data:
                errors = []
                for e in data['detail']:
                    ctx = e.get('ctx', {})
                    if not ctx.get('error') and e.get('msg'):
                        msg = e['msg'].partition(', ')[2]
                        ctx['error'] = msg
                    error = InitErrorDetails(type=e['type'], loc=tuple(e['loc']), input=e.get('input'), ctx=ctx)
                    errors.append(error)
                raise ValidationError.from_exception_data(f'endpoint {endpoint}', line_errors=errors)
        if not response.ok:
            raise RuntimeError(f'Error {response.status_code} from Tesseract: {response.text}')
        data = response.json()
        if endpoint in ['apply', 'jacobian', 'jacobian_vector_product', 'vector_jacobian_product']:
            data = _tree_map(_decode_array, data, is_leaf=lambda x: type(x) is dict and 'shape' in x)
        return data

    def run_tesseract(self, endpoint: str, payload: dict | None=None, run_id: str | None=None) -> dict:
        """Run a Tesseract endpoint.

        Args:
            endpoint: The endpoint to run.
            payload: The payload to send to the endpoint.
            run_id: a string to identify the run. Run outputs will be located
                    in a directory suffixed with this id.

        Returns:
            The loaded JSON response from the endpoint, with decoded arrays.
        """
        if endpoint in ['openapi_schema', 'health']:
            method = 'GET'
        else:
            method = 'POST'
        if endpoint == 'openapi_schema':
            endpoint = 'openapi.json'
        return self._request(endpoint, method, payload, run_id)