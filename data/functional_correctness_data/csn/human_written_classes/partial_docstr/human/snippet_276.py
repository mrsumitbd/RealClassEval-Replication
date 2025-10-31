from rest_framework.reverse import reverse
from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch
from rest_framework_json_api.utils import Hyperlink, format_link_segment, get_resource_type_from_instance, get_resource_type_from_queryset, get_resource_type_from_serializer

class HyperlinkedMixin:
    self_link_view_name = None
    related_link_view_name = None
    related_link_lookup_field = 'pk'

    def __init__(self, self_link_view_name=None, related_link_view_name=None, **kwargs):
        if self_link_view_name is not None:
            self.self_link_view_name = self_link_view_name
        if related_link_view_name is not None:
            self.related_link_view_name = related_link_view_name
        self.related_link_lookup_field = kwargs.pop('related_link_lookup_field', self.related_link_lookup_field)
        self.related_link_url_kwarg = kwargs.pop('related_link_url_kwarg', self.related_link_lookup_field)
        self.reverse = reverse
        super().__init__(**kwargs)

    def get_url(self, name, view_name, kwargs, request):
        """
        Given a name, view name and kwargs, return the URL that hyperlinks to the object.

        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        if not view_name:
            return None
        try:
            url = self.reverse(view_name, kwargs=kwargs, request=request)
        except NoReverseMatch:
            msg = 'Could not resolve URL for hyperlinked relationship using view name "%s".'
            raise ImproperlyConfigured(msg % view_name)
        if url is None:
            return None
        return Hyperlink(url, name)

    def get_links(self, obj=None, lookup_field='pk'):
        request = self.context.get('request', None)
        view = self.context.get('view', None)
        return_data = {}
        kwargs = {lookup_field: getattr(obj, lookup_field) if obj else view.kwargs[lookup_field]}
        field_name = self.field_name if self.field_name else self.parent.field_name
        self_kwargs = kwargs.copy()
        self_kwargs.update({'related_field': format_link_segment(field_name)})
        self_link = self.get_url('self', self.self_link_view_name, self_kwargs, request)
        if self.related_link_url_kwarg == 'pk':
            related_kwargs = self_kwargs
        else:
            related_kwargs = {self.related_link_url_kwarg: kwargs[self.related_link_lookup_field]}
        related_link = self.get_url('related', self.related_link_view_name, related_kwargs, request)
        if self_link:
            return_data.update({'self': self_link})
        if related_link:
            return_data.update({'related': related_link})
        return return_data