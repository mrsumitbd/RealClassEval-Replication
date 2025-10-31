from django.http import Http404
from rest_framework_extensions.settings import extensions_api_settings
import uuid
from django.core.exceptions import ValidationError

class NestedViewSetMixin:

    def get_queryset(self):
        return self.filter_queryset_by_parents_lookups(super().get_queryset())

    def filter_queryset_by_parents_lookups(self, queryset):
        parents_query_dict = self.get_parents_query_dict()
        if parents_query_dict:
            try:
                cleaned_dict = {}
                for key, value in parents_query_dict.items():
                    if 'uuid' in key.lower() or key.endswith('_code'):
                        try:
                            cleaned_dict[key] = uuid.UUID(str(value))
                        except ValueError:
                            raise Http404
                    else:
                        cleaned_dict[key] = value
                return queryset.filter(**cleaned_dict)
            except (ValueError, ValidationError):
                raise Http404
        else:
            return queryset

    def get_parents_query_dict(self):
        result = {}
        for kwarg_name, kwarg_value in self.kwargs.items():
            if kwarg_name.startswith(extensions_api_settings.DEFAULT_PARENT_LOOKUP_KWARG_NAME_PREFIX):
                query_lookup = kwarg_name.replace(extensions_api_settings.DEFAULT_PARENT_LOOKUP_KWARG_NAME_PREFIX, '', 1)
                query_value = kwarg_value
                result[query_lookup] = query_value
        return result