from rest_framework.response import Response
from rest_framework import status

class PatchModelMixin:
    """
    Patch model instance, or requested filtered queryset.

    Route PATCH request method to `modify_obj` or `modify_set`. Override `perform_modify` if necessary.

    Default methods return 204 no content.
    """

    def modify_set(self, request, *args, **kwargs):
        return self.modify_queryset(request, self.filter_queryset(self.get_queryset()))

    def modify_obj(self, request, *args, **kwargs):
        return self.modify_queryset(request, self.get_object())

    def modify_queryset(self, request, queryset):
        patch = Patch(self.get_serializer(), data=request.data)
        patch.is_valid(raise_exception=True)
        self.perform_modify(queryset, patch)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_modify(self, queryset, patch):
        """ actually perform update on queryset """
        patch.update_queryset(queryset)