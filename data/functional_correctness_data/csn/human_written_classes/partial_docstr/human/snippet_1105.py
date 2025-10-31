from pydantic._internal import _schema_generation_shared
from pydantic_core import core_schema
from pydantic.json_schema import JsonSchemaValue
from pydantic import BeforeValidator, Field, GetCoreSchemaHandler
from typing import Any, List, Type, TypeVar, Union

class SemiStrictBool:
    __slots__ = ()

    def __new__(cls, value: Any) -> bool:
        """
        Ensure that we only allow bools.
        """
        if isinstance(value, bool):
            return value
        if isinstance(value, str) and value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        raise ValueError("Value given can't be validated as bool")

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: core_schema.CoreSchema, handler: _schema_generation_shared.GetJsonSchemaHandler) -> JsonSchemaValue:
        field_schema = {}
        field_schema.update(type='boolean')
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, _source: Type[Any], _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls._validate, serialization=core_schema.to_string_ser_schema())

    @classmethod
    def _validate(cls, input_value: Any) -> bool:
        return cls(input_value)