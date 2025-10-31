import pydantic
from pydantic_core import PydanticUndefined


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
        if not isinstance(data, dict):
            return data

        keep_serial_keys = set(self._keep_these_fields() or ())

        fields = getattr(self, 'model_fields', {}) or {}
        alias_to_name = {}
        for name, finfo in fields.items():
            alias = getattr(finfo, 'alias', None) or name
            alias_to_name[alias] = name

        keep_names = set()
        for k in keep_serial_keys:
            if k in fields:
                keep_names.add(k)
            elif k in alias_to_name:
                keep_names.add(alias_to_name[k])

        filtered = {}
        for key, value in data.items():
            if key in keep_serial_keys:
                filtered[key] = value
                continue

            field_name = None
            if key in alias_to_name:
                field_name = alias_to_name[key]
            elif key in fields:
                field_name = key

            if not field_name:
                filtered[key] = value
                continue

            finfo = fields[field_name]
            has_default = True
            default_value = None

            if getattr(finfo, 'default', PydanticUndefined) is not PydanticUndefined:
                default_value = finfo.default
            elif getattr(finfo, 'default_factory', None) is not None:
                try:
                    default_value = finfo.default_factory()
                except TypeError:
                    has_default = False
            else:
                has_default = False

            if field_name in keep_names:
                filtered[key] = value
                continue

            if has_default and value == default_value:
                continue

            filtered[key] = value

        return filtered

    def _keep_these_fields(self) -> tuple[str]:
        '''
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON.
        This is necessary for round-tripping to JSON when there are fields that
        determine which dataclass to use for deserialization.
        '''
        return ()
