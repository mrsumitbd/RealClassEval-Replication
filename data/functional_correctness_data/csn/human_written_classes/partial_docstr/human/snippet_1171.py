import marshmallow as ma
from pyramid.response import Response

class PartialUpdateMixin:
    """
    Support for partially updating instance (PATCH).
    """

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        schema = self.get_schema(context={'instance': instance})
        try:
            data, errors = schema.load(request.json_body, partial=True)
        except ma.ValidationError as err:
            return Response(json_body=err.messages, status=400)
        self.perform_partial_update(data, instance)
        content = schema.dump(instance)[0]
        return Response(json=content)

    def perform_partial_update(self, data, instance):
        """
        Hook for controlling the update of an model instance. Override this if you need to do more with your
        data before updating the object than just mapping the deserialized data to the attribute of the instance.
        """
        for key, val in data.items():
            setattr(instance, key, val)