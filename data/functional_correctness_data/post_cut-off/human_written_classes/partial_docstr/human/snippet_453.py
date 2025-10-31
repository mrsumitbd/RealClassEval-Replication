from pydantic import BaseModel, TypeAdapter, ValidationError
from types import ModuleType
import traceback

class LocalClient:
    """Local Client for Tesseracts."""

    def __init__(self, tesseract_api: ModuleType) -> None:
        from tesseract_core.runtime.core import create_endpoints
        from tesseract_core.runtime.serve import create_rest_api
        self._endpoints = {func.__name__: func for func in create_endpoints(tesseract_api)}
        self._openapi_schema = create_rest_api(tesseract_api).openapi()

    def run_tesseract(self, endpoint: str, payload: dict | None=None, run_id: str | None=None) -> dict:
        """Run a Tesseract endpoint.

        Args:
            endpoint: The endpoint to run.
            payload: The payload to send to the endpoint.
            run_id: a string to identify the run.

        Returns:
            The loaded JSON response from the endpoint, with decoded arrays.
        """
        if endpoint == 'openapi_schema':
            return self._openapi_schema
        if endpoint not in self._endpoints:
            raise RuntimeError(f'Endpoint {endpoint} not found in Tesseract API.')
        func = self._endpoints[endpoint]
        InputSchema = func.__annotations__.get('payload', None)
        OutputSchema = func.__annotations__.get('return', None)
        if InputSchema is not None:
            parsed_payload = InputSchema.model_validate(payload)
        else:
            parsed_payload = None
        try:
            if parsed_payload is not None:
                result = self._endpoints[endpoint](parsed_payload)
            else:
                result = self._endpoints[endpoint]()
        except Exception as ex:
            tb = traceback.format_exc()
            raise RuntimeError(f'{tb}\nError running Tesseract API {endpoint}: {ex} (see above for full traceback)') from None
        if OutputSchema is not None:
            if isinstance(OutputSchema, type) and issubclass(OutputSchema, BaseModel):
                result = OutputSchema.model_validate(result).model_dump()
            else:
                result = TypeAdapter(OutputSchema).validate_python(result)
        return result