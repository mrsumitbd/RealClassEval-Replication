from chamber.forms.validators import RestrictedFileValidator, AllowedContentTypesByFilenameFileValidator, AllowedContentTypesByContentFileValidator
from chamber.config import settings

class RestrictedFileFieldMixin:
    """
    Same as FileField, but you can specify:
        * allowed_content_types - list of allowed content types. Example: ['application/json', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload in MB.
    """

    def __init__(self, *args, **kwargs):
        max_upload_size = kwargs.pop('max_upload_size', settings.MAX_FILE_UPLOAD_SIZE) * 1024 * 1024
        allowed_content_types = kwargs.pop('allowed_content_types', None)
        super().__init__(*args, **kwargs)
        self.validators.append(RestrictedFileValidator(max_upload_size))
        if allowed_content_types:
            self.validators = tuple(self.validators) + (AllowedContentTypesByFilenameFileValidator(allowed_content_types), AllowedContentTypesByContentFileValidator(allowed_content_types))

    def generate_filename(self, instance, filename):
        """
        removes UTF chars from filename
        """
        from unidecode import unidecode
        return super().generate_filename(instance, unidecode(str(filename)))