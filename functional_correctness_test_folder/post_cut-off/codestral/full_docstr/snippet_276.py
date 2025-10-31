
import pydantic


class NoDefaultsMixin:
    @pydantic.model_serializer(mode='wrap')
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        result = nxt(self)
        if not hasattr(self, '_keep_these_fields'):
            return result
        keep_fields = self._keep_these_fields()
        if not keep_fields:
            return result
        return {k: v for k, v in result.items() if k in keep_fields}

    def _keep_these_fields(self) -> tuple[str]:
        return ()
