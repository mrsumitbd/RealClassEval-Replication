import pydantic
from pydantic.fields import PydanticUndefined


class NoDefaultsMixin:
    '''
    Mixin so that we don't need to copy and paste the code to avoid filling JSON values
    with a full catalog of the default values of rarely-used fields.
    '''
    @pydantic.model_serializer(mode='wrap')
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        data = nxt(self)
        if not isinstance(data, dict):
            return data

        keep = set(self._keep_these_fields() or ())

        try:
            fields = type(self).model_fields
        except AttributeError:
            return data

        for name, field in fields.items():
            out_key = getattr(field, 'serialization_alias', None) or getattr(
                field, 'alias', None) or name

            # Allow keeping by either internal or external name
            if out_key in keep or name in keep:
                continue
            if out_key not in data:
                continue

            remove = False
            if field.default is not PydanticUndefined:
                try:
                    if data[out_key] == field.default:
                        remove = True
                except Exception:
                    pass
            elif field.default_factory is not None:
                try:
                    default_value = field.default_factory()
                    if data[out_key] == default_value:
                        remove = True
                except Exception:
                    pass

            if remove:
                data.pop(out_key, None)

        return data

    def _keep_these_fields(self) -> tuple[str]:
        '''
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON.
        This is necessary for round-tripping to JSON when there are fields that
        determine which dataclass to use for deserialization.
        '''
        return ()
