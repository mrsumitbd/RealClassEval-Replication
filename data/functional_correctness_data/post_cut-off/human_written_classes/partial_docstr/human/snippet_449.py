from tesseract_core.runtime.file_interactions import PathLike, parent_path
from pydantic import AfterValidator, GetCoreSchemaHandler, GetJsonSchemaHandler, TypeAdapter
import json
from collections.abc import Iterator, Sequence
from typing import Annotated, Any, Callable, Union, get_args, get_origin
from tesseract_core.runtime.schema_types import safe_issubclass
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, SchemaSerializer, SchemaValidator, core_schema

class PydanticLazySequenceAnnotation:
    """Pydantic annotation for lazy sequences."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        raise RuntimeError(f'{self.__class__.__name__} cannot be instantiated')

    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        """This method is called by Pydantic to get the core schema for the annotated type.

        Does most of the heavy lifting for validation and serialization.
        """

        def create_sequence(maybe_path: Union[str, Sequence[Any]]) -> LazySequence:
            """Expand a glob pattern into a LazySequence if needed."""
            validator = SchemaValidator(item_schema)
            if not isinstance(maybe_path, str) or not maybe_path.startswith('@'):
                items = maybe_path
                getter = validator.validate_python
                return LazySequence(items, getter)
            from .file_interactions import expand_glob, read_from_path
            maybe_path = maybe_path[1:]
            items = expand_glob(maybe_path)

            def load_item(key: str) -> Any:
                buffer = read_from_path(key)
                obj = json.loads(buffer.decode('utf-8'))
                context = {'base_dir': parent_path(key)}
                return validator.validate_python(obj, context=context)
            return LazySequence(items, load_item)

        def serialize(obj: LazySequence, __info: Any) -> Any:
            """When serializing, convert the LazySequence to a list of items.

            This is not an encouraged use case, but it is supported for completeness.
            """
            materialized_sequence = list(obj)
            serializer = SchemaSerializer(sequence_schema)
            return serializer.to_python(materialized_sequence, **__info.__dict__)
        origin = get_origin(_source_type)
        if not safe_issubclass(origin, Sequence):
            raise ValueError(f'LazySequence can only be used with Sequence types, not {origin}')
        args = get_args(_source_type)
        assert len(args) == 1
        item_schema = TypeAdapter(args[0]).core_schema
        sequence_schema = _handler(_source_type)
        obj_or_path = core_schema.union_schema([sequence_schema, core_schema.str_schema(pattern='^@')])
        load_schema = core_schema.chain_schema([obj_or_path, core_schema.no_info_plain_validator_function(create_sequence, serialization=core_schema.plain_serializer_function_ser_schema(serialize, info_arg=True, return_schema=sequence_schema))])
        return core_schema.json_or_python_schema(json_schema=load_schema, python_schema=load_schema, serialization=core_schema.plain_serializer_function_ser_schema(serialize, info_arg=True))

    @classmethod
    def __get_pydantic_json_schema__(cls, _core_schema: core_schema.CoreSchema, handler: GetJsonSchemaHandler) -> JsonSchemaValue:
        """This method is called by Pydantic to get the JSON schema for the annotated type."""
        return handler(_core_schema)