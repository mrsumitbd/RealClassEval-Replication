
import pydantic


class NoDefaultsMixin:

    @pydantic.model_serializer(mode='wrap')
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        def serialize_without_defaults(self):
            data = nxt(self)
            fields_to_keep = self._keep_these_fields()
            return {k: v for k, v in data.items() if k in fields_to_keep}
        return serialize_without_defaults

    def _keep_these_fields(self) -> tuple[str]:
        return tuple(self.__pydantic_root_model__.model_fields.keys())
