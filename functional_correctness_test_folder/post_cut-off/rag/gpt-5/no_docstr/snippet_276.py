import dataclasses
from typing import Any, Dict, Mapping, Tuple
import pydantic


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
        out = nxt(self)
        if not isinstance(out, dict):
            return out

        # Build a mapping of field metadata so we can detect defaults.
        # Support both BaseModel (model_fields) and pydantic.dataclasses (__pydantic_fields__).
        fields_map: Mapping[str, Any] = getattr(
            type(self), 'model_fields', None)
        if not fields_map:
            fields_map = getattr(type(self), '__pydantic_fields__', None)

        # If we can't introspect fields, return as-is.
        if not fields_map:
            return out

        # Build alias->name mapping for correct key lookup regardless of serialization alias.
        alias_to_name: Dict[str, str] = {}
        for name, fi in fields_map.items():
            alias = getattr(fi, 'serialization_alias', None)
            if not alias:
                alias = getattr(fi, 'alias', None)  # legacy attribute fallback
            alias_to_name[alias or name] = name

        keep_set = set(self._keep_these_fields())

        # Helper to obtain a field's default value if it exists; returns a sentinel otherwise.
        _NO_DEFAULT = object()

        def default_for_field(field_info: Any) -> Any:
            # Pydantic FieldInfo API (v2)
            if hasattr(field_info, 'default_factory') and field_info.default_factory is not None:
                try:
                    return field_info.default_factory()
                except Exception:
                    return _NO_DEFAULT
            if getattr(field_info, 'is_required', None) is True:
                return _NO_DEFAULT
            if hasattr(field_info, 'default'):
                return field_info.default
            # dataclasses.Field fallback
            if isinstance(field_info, dataclasses.Field):
                if field_info.default is not dataclasses.MISSING:
                    return field_info.default
                if field_info.default_factory is not dataclasses.MISSING:
                    try:
                        return field_info.default_factory()
                    except Exception:
                        return _NO_DEFAULT
            return _NO_DEFAULT

        # Remove keys whose current value equals the default, unless explicitly kept.
        for serialized_key in list(out.keys()):
            name = alias_to_name.get(serialized_key, serialized_key)
            if name in keep_set:
                continue
            fi = fields_map.get(name)
            if fi is None:
                continue
            default_val = default_for_field(fi)
            if default_val is _NO_DEFAULT:
                continue
            current_val = getattr(self, name, out[serialized_key])
            try:
                equal = current_val == default_val
            except Exception:
                equal = False
            if equal:
                out.pop(serialized_key, None)

        return out

    def _keep_these_fields(self) -> tuple[str]:
        '''
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON.
        This is necessary for round-tripping to JSON when there are fields that
        determine which dataclass to use for deserialization.
        '''
        return tuple()
