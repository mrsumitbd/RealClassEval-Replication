
import pydantic


class NoDefaultsMixin:
    '''
    Mixin so that we don't need to copy and paste the code to avoid filling JSON values
    with a full catalog of the default values of rarely-used fields.
    '''
    @pydantic.model_serializer(mode='wrap')
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        data = nxt(self)
        keep = set(self._keep_these_fields())
        # Only keep fields that are in keep, or that are not default values
        # We assume that nxt(self) returns a dict of all fields
        # We want to remove fields that are at their default value, unless in keep
        # To do this, we need to compare each field's value to its default
        # We'll use self.__fields_set__ to know which fields were set, but for
        # completeness, we check all fields
        model = type(self)
        result = {}
        for k, v in data.items():
            if k in keep:
                result[k] = v
            else:
                # Get default value for this field, if any
                default = None
                if k in model.model_fields:
                    field_info = model.model_fields[k]
                    if field_info.default_factory is not None:
                        default = field_info.default_factory()
                    else:
                        default = field_info.default
                if v != default:
                    result[k] = v
        return result

    def _keep_these_fields(self) -> tuple[str]:
        '''
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON.
        This is necessary for round-tripping to JSON when there are fields that
        determine which dataclass to use for deserialization.
        '''
        return ()
