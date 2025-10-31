
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
        def wrapped(instance, *args, **kwargs):
            # Call the next serializer to get the dict
            data = nxt(instance, *args, **kwargs)
            # Remove fields that are set to their default values, unless in _keep_these_fields
            keep = set(instance._keep_these_fields())
            # Get the model fields and their defaults
            model = type(instance)
            # Pydantic v2: model.model_fields is a dict of field name -> FieldInfo
            for field_name, field_info in model.model_fields.items():
                if field_name in keep:
                    continue
                default = field_info.default
                # If the field is not set or is set to its default, remove it
                if field_name in data:
                    value = getattr(instance, field_name, None)
                    # Remove if value is default (but not if default is .../missing)
                    if default is not pydantic._internal._fields.PydanticUndefined and value == default:
                        del data[field_name]
            return data
        return wrapped

    def _keep_these_fields(self) -> tuple[str]:
        '''
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON.
        This is necessary for round-tripping to JSON when there are fields that
        determine which dataclass to use for deserialization.
        '''
        return ()
