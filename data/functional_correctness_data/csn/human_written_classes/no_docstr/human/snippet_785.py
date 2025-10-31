from rest_framework.viewsets import ViewSetMixin
from typing import TYPE_CHECKING, Any, Type, cast

class BananasBaseRouter:

    def get_default_basename(self, viewset: Type[ViewSetMixin]) -> str:
        return cast(Type['BananasAPI'], viewset).get_admin_meta().basename

    def get_schema_view(self) -> Any:
        raise NotImplementedError