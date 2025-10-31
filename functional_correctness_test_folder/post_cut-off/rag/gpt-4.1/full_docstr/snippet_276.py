
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
        # We want to filter out fields that have default values, unless they are in _keep_these_fields
        def serializer(instance, info):
            data = nxt(instance, info)
            keep = set(instance._keep_these_fields())
            # Only keep fields that are not default, or are in keep
            # Pydantic v2: instance.model_fields gives field info
            for field_name, field in instance.__class__.model_fields.items():
                if field_name in data:
                    value = getattr(instance, field_name)
                    if field.default is not pydantic._internal._fields.PydanticUndefined:
                        if value == field.default and field_name not in keep:
                            data.pop(field_name)
            return data
        return serializer

    def _keep_these_fields(self) -> tuple[str]:
        '''
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON.
        This is necessary for round-tripping to JSON when there are fields that
        determine which dataclass to use for deserialization.
        '''
        return ()
