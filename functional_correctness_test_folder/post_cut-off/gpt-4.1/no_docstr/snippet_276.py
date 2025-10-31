
import pydantic


class NoDefaultsMixin:

    @pydantic.model_serializer(mode='wrap')
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        data = nxt()
        keep = set(self._keep_these_fields())
        return {k: v for k, v in data.items() if k in keep}

    def _keep_these_fields(self) -> tuple[str]:
        return tuple(self.__fields__.keys())
