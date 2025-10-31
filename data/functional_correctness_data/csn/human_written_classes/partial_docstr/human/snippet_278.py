from rest_framework.exceptions import ParseError
from rest_framework_json_api.utils import get_included_resources, get_resource_type_from_instance, get_resource_type_from_model, get_resource_type_from_serializer, undo_format_field_name

class IncludedResourcesValidationMixin:
    """
    A serializer mixin that adds validation of `include` query parameter to
    support compound documents.

    Specification: https://jsonapi.org/format/#document-compound-documents)
    """

    def __init__(self, *args, **kwargs):
        context = kwargs.get('context')
        request = context.get('request') if context else None
        view = context.get('view') if context else None

        def validate_path(serializer_class, field_path, path):
            serializers = getattr(serializer_class, 'included_serializers', None)
            if serializers is None:
                raise ParseError('This endpoint does not support the include parameter')
            this_field_name = field_path[0]
            this_included_serializer = serializers.get(this_field_name)
            if this_included_serializer is None:
                raise ParseError('This endpoint does not support the include parameter for path {}'.format(path))
            if len(field_path) > 1:
                new_included_field_path = field_path[1:]
                validate_path(this_included_serializer, new_included_field_path, path)
        if request and view:
            included_resources = get_included_resources(request)
            for included_field_name in included_resources:
                included_field_path = included_field_name.split('.')
                if 'related_field' in view.kwargs:
                    this_serializer_class = view.get_related_serializer_class()
                else:
                    this_serializer_class = view.get_serializer_class()
                validate_path(this_serializer_class, included_field_path, included_field_name)
        super().__init__(*args, **kwargs)