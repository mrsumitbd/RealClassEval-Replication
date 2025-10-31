import pydantic
from typing import Tuple


class NoDefaultsMixin:
    @pydantic.model_serializer(mode='wrap')
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        data = nxt(self)
        if not isinstance(data, dict):
            return data
        keep = set(self._keep_these_fields() or ())
        fields_set = getattr(self, '__pydantic_fields_set__', set())
        if not isinstance(fields_set, set):
            try:
                fields_set = set(fields_set)
            except Exception:
                fields_set = set()
        return {k: v for k, v in data.items() if (k in keep) or (k in fields_set)}

    def _keep_these_fields(self) -> Tuple[str, ...]:
        return ()
