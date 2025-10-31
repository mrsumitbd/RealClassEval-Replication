from pyramid.response import Response

class DestroyModelMixin:
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=204)

    def perform_destroy(self, instance):
        """
        Hook for controlling the deletion of an model instance. Override this if you need to do more than just
        delete the instance.
        """
        self.request.dbsession.delete(instance)