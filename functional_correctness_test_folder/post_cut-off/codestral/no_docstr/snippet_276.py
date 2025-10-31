
import pydantic


class NoDefaultsMixin:

    @pydantic.model_serializer(mode='wrap')
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        return nxt()

    def _keep_these_fields(self) -> tuple[str]:
        return ()
