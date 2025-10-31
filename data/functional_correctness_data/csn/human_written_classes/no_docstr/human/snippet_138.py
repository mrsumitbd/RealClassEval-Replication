from actstream.models import Action, model_stream, user_stream, any_stream
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

class ModelActivityMixin:

    def get_object(self, request, content_type_id):
        return get_object_or_404(ContentType, pk=content_type_id).model_class()

    def get_stream(self):
        return model_stream