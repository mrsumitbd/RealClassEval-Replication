
from typing import Any
import pydantic


class NoDefaultsMixin:

    @pydantic.model_serializer(mode='wrap')
    def _workaround_for_design_flaw_in_pydantic(self, nxt: Any) -> Any:
        result = nxt(self)
        if hasattr(self, '_keep_these_fields'):
            fields_to_keep = self._keep_these_fields()
            return {k: v for k, v in result.items() if k in fields_to_keep}
        return result

    def _keep_these_fields(self) -> tuple[str]:
        return ()
