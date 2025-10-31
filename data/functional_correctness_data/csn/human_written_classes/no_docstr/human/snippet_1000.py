from django.utils.translation import gettext
import magic
from django.core.exceptions import ValidationError

class AllowedContentTypesByContentFileValidator:

    def __init__(self, content_types):
        self.content_types = content_types

    def __call__(self, data):
        data.open()
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
            mime_type = m.id_buffer(data.read(2048))
            data.seek(0)
            if mime_type not in self.content_types:
                raise ValidationError(gettext('File content was evaluated as not supported file type'))
        return data