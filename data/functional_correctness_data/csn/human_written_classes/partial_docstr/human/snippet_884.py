class RelatedId:
    """Resolve a related item by a scalar ID.

    :param view_class: The :py:class:`ModelView` corresponding to the related
        model.
    :param str field_name: The field name on request data.
    """

    def __init__(self, view_class, field_name):
        self._view_class = view_class
        self.field_name = field_name

    def create_view(self):
        return self._view_class()

    def resolve_related_id(self, view, id):
        return view.resolve_related_id(id)