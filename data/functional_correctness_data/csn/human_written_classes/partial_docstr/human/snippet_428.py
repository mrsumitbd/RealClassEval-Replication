import json
from django.core.serializers.json import DjangoJSONEncoder
from django.core import serializers
from django.http import HttpResponse, StreamingHttpResponse
from django.core.exceptions import ImproperlyConfigured, PermissionDenied

class JSONResponseMixin:
    """
    A mixin that allows you to easily serialize simple data such as a dict or
    Django models.
    """
    content_type = None
    json_dumps_kwargs = None
    json_encoder_class = DjangoJSONEncoder

    def get_content_type(self):
        if self.content_type is not None and (not isinstance(self.content_type, ((str,), str))):
            raise ImproperlyConfigured('{0} is missing a content type. Define {0}.content_type, or override {0}.get_content_type().'.format(self.__class__.__name__))
        return self.content_type or 'application/json'

    def get_json_dumps_kwargs(self):
        if self.json_dumps_kwargs is None:
            self.json_dumps_kwargs = {}
        self.json_dumps_kwargs.setdefault('ensure_ascii', False)
        return self.json_dumps_kwargs

    def render_json_response(self, context_dict, status=200):
        """
        Limited serialization for shipping plain data. Do not use for models
        or other complex or custom objects.
        """
        json_context = json.dumps(context_dict, cls=self.json_encoder_class, **self.get_json_dumps_kwargs()).encode('utf-8')
        return HttpResponse(json_context, content_type=self.get_content_type(), status=status)

    def render_json_object_response(self, objects, **kwargs):
        """
        Serializes objects using Django's builtin JSON serializer. Additional
        kwargs can be used the same way for django.core.serializers.serialize.
        """
        json_data = serializers.serialize('json', objects, **kwargs)
        return HttpResponse(json_data, content_type=self.get_content_type())