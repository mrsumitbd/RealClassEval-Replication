import marshmallow as ma
from pyramid.response import Response

class CreateModelMixin:
    """
    Create object from serialized data.
    """

    def create(self, request, *args, **kwargs):
        schema = self.get_schema()
        try:
            data, errors = schema.load(request.json_body)
        except ma.ValidationError as err:
            return Response(json=err.messages, status=400)
        instance = self.perform_create(data)
        content = schema.dump(instance)[0]
        return Response(json=content, status=201)

    def perform_create(self, data):
        """
        Hook for controlling the creation of an model instance. Override this if you need to do more with your
        data before saving your object than just mapping the deserialized data to a new instance of ``self.model``.
        """
        instance = self.model(**data)
        self.request.dbsession.add(instance)
        self.request.dbsession.flush()
        return instance