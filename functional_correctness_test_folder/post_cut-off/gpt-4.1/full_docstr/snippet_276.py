
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
        # Call the next serializer to get the dict
        data = nxt(self)
        # Only keep fields that are not set to their default values,
        # unless they are in _keep_these_fields()
        keep_fields = set(self._keep_these_fields())
        model_fields = self.__class__.__pydantic_fields__
        result = {}
        for k, v in data.items():
            if k in keep_fields:
                result[k] = v
            else:
                field = model_fields.get(k)
                if field is not None:
                    if field.default is not pydantic._internal._fields.Undefined:
                        if v != field.default:
                            result[k] = v
                    elif field.default_factory is not None:
                        if v != field.default_factory():
                            result[k] = v
                    else:
                        # No default, always include
                        result[k] = v
                else:
                    # Not a model field, just include
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
