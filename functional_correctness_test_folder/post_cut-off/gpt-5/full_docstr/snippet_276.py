class NoDefaultsMixin:
    '''
    Mixin so that we don't need to copy and paste the code to avoid filling JSON values
    with a full catalog of the default values of rarely-used fields.
    '''
    @pydantic.model_serializer(mode='wrap')
    def _workaround_for_design_flaw_in_pydantic(self, nxt, info):
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
        # Prefer excluding unset fields to avoid dumping defaults
        try:
            data = nxt(self, info, exclude_unset=True)
        except TypeError:
            # Fallbacks for potential signature differences across pydantic versions
            try:
                data = nxt(self, exclude_unset=True)
            except TypeError:
                data = nxt(self)

        # Ensure explicitly requested fields are kept even if they were not set,
        # e.g., discriminators needed for round-tripping.
        for field in self._keep_these_fields():
            if field not in data:
                data[field] = getattr(self, field, None)

        return data

    def _keep_these_fields(self) -> tuple[str, ...]:
        '''
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON.
        This is necessary for round-tripping to JSON when there are fields that
        determine which dataclass to use for deserialization.
        '''
        return ()
