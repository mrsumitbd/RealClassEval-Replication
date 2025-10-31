from openapi_spec_validator.validation.types import SpecValidatorType
from typing import Iterator
from jsonschema.exceptions import ValidationError
from jsonschema_path.typing import Schema
from typing import Optional
import warnings

class SpecValidatorProxy:

    def __init__(self, cls: SpecValidatorType, deprecated: str='SpecValidator', use: Optional[str]=None):
        self.cls = cls
        self.deprecated = deprecated
        self.use = use or self.cls.__name__

    def validate(self, schema: Schema, base_uri: str='', spec_url: Optional[str]=None) -> None:
        for err in self.iter_errors(schema, base_uri=base_uri, spec_url=spec_url):
            raise err

    def is_valid(self, schema: Schema) -> bool:
        error = next(self.iter_errors(schema), None)
        return error is None

    def iter_errors(self, schema: Schema, base_uri: str='', spec_url: Optional[str]=None) -> Iterator[ValidationError]:
        warnings.warn(f'{self.deprecated} is deprecated. Use {self.use} instead.', DeprecationWarning)
        validator = self.cls(schema, base_uri=base_uri, spec_url=spec_url)
        return validator.iter_errors()