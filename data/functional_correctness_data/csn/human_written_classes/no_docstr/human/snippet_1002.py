from django.utils.translation import gettext
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

class RestrictedFileValidator:

    def __init__(self, max_upload_size):
        self.max_upload_size = max_upload_size

    def __call__(self, data):
        if data.size > self.max_upload_size:
            raise ValidationError(gettext('Please keep filesize under {max}. Current filesize {current}').format(max=filesizeformat(self.max_upload_size), current=filesizeformat(data.size)))
        else:
            return data