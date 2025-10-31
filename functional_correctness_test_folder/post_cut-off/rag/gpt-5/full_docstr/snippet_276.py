import dataclasses
from typing import Mapping

import pydantic


# Try to import undefined sentinel across pydantic versions
try:
    from pydantic_core import PydanticUndefined
except Exception:
    try:
        from pydantic.fields import Undefined as PydanticUndefined  # type: ignore
    except Exception:
        class _UndefinedSentinel:  # fallback unique sentinel
            pass
        PydanticUndefined = _UndefinedSentinel()


class NoDefaultsMixin:
    '''
    Mixin so that we don't need to copy and paste the code to avoid filling JSON values
    with a full catalog of the default values of rarely-used fields.
    '''
    @pydantic.model_serializer(mode='wrap')
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        '''
        Workaround for a design flaw in Pydantic that forces users to accept
        unnecessary garbage in their serialized JSON data or to override
        poorly-documented serialization hooks repeatedly.  Automates overriding said
        poorly-documented serialization hooks for a single dataclass.
        See https://github.com/pydantic/pydantic/issues/4554 for the relevant dismissive
        comment from the devs. This comment suggests overriding :func:`dict()`, but that
        method was disabled a year later. Now you need to add a custom serializer method
        with a ``@model_serializer`` decorator.
        See the docs at
        https://docs.pydantic.dev/latest/api/functional_serializers/
        for some dubious information on how this API works.
        See comments below for important gotchas that aren't in the documentation.
        '''
        data = nxt(self)
        if not isinstance(data, Mapping):
            return data

        keep = set(self._keep_these_fields() or ())

        # Build a uniform iterable of field specs: (name, default_exists, default_value, alias)
        field_specs = []

        # pydantic v2 BaseModel
        model_fields = getattr(self.__class__, 'model_fields', None)
        if isinstance(model_fields, dict):
            for name, field in model_fields.items():
                alias = getattr(field, 'alias', None)
                default_exists = False
                default_val = None
                default_factory = getattr(field, 'default_factory', None)
                if default_factory is not None:
                    try:
                        default_val = default_factory()
                        default_exists = True
                    except Exception:
                        default_exists = False
                else:
                    if getattr(field, 'default', PydanticUndefined) is not PydanticUndefined:
                        # type: ignore[attr-defined]
                        default_val = field.default
                        default_exists = True
                field_specs.append((name, default_exists, default_val, alias))

        # pydantic v1 BaseModel
        elif isinstance(getattr(self.__class__, '__fields__', None), dict):
            # type: ignore[attr-defined]
            for name, field in self.__class__.__fields__.items():
                alias = getattr(field, 'alias', None)
                default_exists = False
                default_val = None
                default_factory = getattr(field, 'default_factory', None)
                if default_factory is not None:
                    try:
                        default_val = default_factory()
                        default_exists = True
                    except Exception:
                        default_exists = False
                else:
                    if not getattr(field, 'required', False):
                        default_val = getattr(field, 'default', None)
                        default_exists = True
                field_specs.append((name, default_exists, default_val, alias))

        # Standard dataclasses (including pydantic.dataclasses)
        elif dataclasses.is_dataclass(self):
            for f in dataclasses.fields(self):
                name = f.name
                alias = None  # dataclasses don't carry alias info in stdlib Fields
                default_exists = False
                default_val = None
                if f.default is not dataclasses.MISSING:
                    default_exists = True
                    default_val = f.default
                # type: ignore[attr-defined]
                elif f.default_factory is not dataclasses.MISSING:
                    try:
                        # type: ignore[attr-defined]
                        default_val = f.default_factory()
                        default_exists = True
                    except Exception:
                        default_exists = False
                field_specs.append((name, default_exists, default_val, alias))

        # Iterate over fields and drop those that are default-valued, unless explicitly kept
        for name, default_exists, default_val, alias in field_specs:
            if name in keep:
                continue
            if not default_exists:
                continue

            try:
                current_py_value = getattr(self, name)
            except Exception:
                current_py_value = data.get(name, data.get(alias))

            try:
                is_default = current_py_value == default_val
            except Exception:
                is_default = False

            if not is_default:
                continue

            # Determine which key is present in the serialized output
            key_to_remove = None
            if name in data:
                key_to_remove = name
            elif alias and alias in data:
                key_to_remove = alias

            if key_to_remove and key_to_remove not in keep:
                try:
                    del data[key_to_remove]
                except Exception:
                    pass

        return data

    def _keep_these_fields(self) -> tuple[str]:
        '''
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON.
        This is necessary for round-tripping to JSON when there are fields that
        determine which dataclass to use for deserialization.
        '''
        return ()
