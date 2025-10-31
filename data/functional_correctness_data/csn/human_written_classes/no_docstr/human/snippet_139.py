from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.contrib.contenttypes.models import ContentType
from actstream.models import Action, model_stream, user_stream, any_stream
from django.shortcuts import get_object_or_404

class ObjectActivityMixin:

    def get_object(self, request, content_type_id, object_id):
        ct = get_object_or_404(ContentType, pk=content_type_id)
        try:
            obj = ct.get_object_for_this_type(pk=object_id)
        except ObjectDoesNotExist:
            raise Http404('No %s matches the given query.' % ct.model_class()._meta.object_name)
        return obj

    def get_stream(self):
        return any_stream