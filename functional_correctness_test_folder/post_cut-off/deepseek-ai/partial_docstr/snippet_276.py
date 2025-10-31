
import pydantic
from typing import Any


class NoDefaultsMixin:
    '''
    Mixin so that we don't need to copy and paste the code to avoid filling JSON values
    with a full catalog of the default values of rarely-used fields.
    '''
    @pydantic.model_serializer(mode='wrap')
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        values = nxt(self)
        fields_to_keep = set(self._keep_these_fields()) if hasattr(
            self, '_keep_these_fields') else set()
        return {k: v for k, v in values.items() if v is not None or k in fields_to_keep}

    def _keep_these_fields(self) -> tuple[str]:
        '''
        Dataclasses that include this mixin can override this method to add specific
        default values to serialized JSON.
        This is necessary for round-tripping to JSON when there are fields that
        determine which dataclass to use for deserialization.
        '''
        return tuple()
