
from pydantic import BaseModel, model_serializer


class NoDefaultsMixin(BaseModel):

    @model_serializer(mode='wrap')
    def _workaround_for_design_flaw_in_pydantic(self, nxt):
        data = nxt(self)
        fields_to_keep = self._keep_these_fields()
        return {field: value for field, value in data.items() if field in fields_to_keep}

    def _keep_these_fields(self) -> tuple[str]:
        return tuple(self.__fields__.keys())
