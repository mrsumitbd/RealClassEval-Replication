from ipaddress import IPv4Network, IPv6Network
from pydantic.json_schema import JsonSchemaValue
from pydantic._internal import _schema_generation_shared
from pydantic_core import core_schema
from pydantic import BeforeValidator, Field, GetCoreSchemaHandler
from typing import Any, List, Type, TypeVar, Union

class LooseIPv4Network:
    __slots__ = ()

    def __new__(cls, value: Any) -> IPv4Network:
        return IPv4Network(value, strict=False)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: core_schema.CoreSchema, handler: _schema_generation_shared.GetJsonSchemaHandler) -> JsonSchemaValue:
        field_schema = {}
        field_schema.update(type='string', format='looseipv4network')
        return field_schema

    @classmethod
    def __get_pydantic_core_schema__(cls, _source: Type[Any], _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls._validate, serialization=core_schema.to_string_ser_schema())

    @classmethod
    def _validate(cls, input_value: Any) -> IPv4Network:
        return cls(input_value)