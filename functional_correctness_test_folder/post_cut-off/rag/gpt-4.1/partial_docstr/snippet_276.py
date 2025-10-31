
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
        # nxt is the next serializer in the chain, which returns a dict of all fields
        # We want to filter out fields that have their default values, unless they are in _keep_these_fields
        def serializer(instance, info):
            # Get the dict as pydantic would serialize it
            data = nxt(instance, info)
            # Get the set of fields to always keep
            keep = set(instance._keep_these_fields())
            # Get the model fields and their default values
            model_fields = instance.__class__.__pydantic_fields__
            # Remove fields that are not in keep and have their default value
            filtered = {}
            for k, v in data.items():
                if k in keep:
                    filtered[k] = v
                else:
                    field = model_fields.get(k)
                    if field is not None:
                        # If the field has a default, and the value matches the default, skip it
                        if field.default is not pydantic._internal._model_construction.PydanticUndefined:
                            if v != field.default:
                                filtered[k] = v
                        elif field.default_factory is not None:
                            # If there's a default_factory, compare to its output
                            try:
                                default_val = field.default_factory()
                                if v != default_val:
                                    filtered[k] = v
                            except Exception:
                                # If default_factory fails, just keep the value
                                filtered[k] = v
                        else:
                            # No default, always keep
                            filtered[k] = v
                    else:
                        # Not a model field, keep it
                        filtered[k] = v
            return filtered
        return serializer

    def _keep_these_fields(self) -> tuple[str]:
        '''
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON.
        This is necessary for round-tripping to JSON when there are fields that
        determine which dataclass to use for deserialization.
        '''
        return ()
