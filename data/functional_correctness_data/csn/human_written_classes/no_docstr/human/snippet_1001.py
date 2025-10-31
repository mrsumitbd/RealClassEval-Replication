from django.core.exceptions import ValidationError
from django.utils.translation import gettext
import mimetypes

class AllowedContentTypesByFilenameFileValidator:

    def __init__(self, content_types):
        self.content_types = content_types

    def __call__(self, data):
        extension_mime_type = mimetypes.guess_type(data.name)[0]
        if extension_mime_type not in self.content_types:
            raise ValidationError(gettext('Extension of file name is not allowed'))
        return data