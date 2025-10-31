from rest_framework.fields import MISSING_ERROR_MESSAGE, Field, SkipField

class SkipDataMixin:
    """
    This workaround skips "data" rendering for relationships
    in order to save some sql queries and improve performance
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_attribute(self, instance):
        raise SkipField

    def to_representation(self, *args):
        raise NotImplementedError