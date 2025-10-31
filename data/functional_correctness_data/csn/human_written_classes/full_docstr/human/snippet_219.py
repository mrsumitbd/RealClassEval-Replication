from django.conf import settings

class RequestParser:
    """Abstract base class, to be implemented by service-specific classes."""

    @property
    def max_file_size(self):
        """The maximum file size to process as an attachment (default=10MB)."""
        return getattr(settings, 'INBOUND_EMAIL_ATTACHMENT_SIZE_MAX', 10000000)

    def parse(self, request):
        """Parse a request object into an EmailMultiAlternatives instance.

        This function is where the hard word gets done. The following fields are
        parsed from the request.POST dict:

        * from - the sender
        * to - the recipient list
        * cc - the cc list
        * html - the HTML version of the email
        * text - the text version of the email
        * subject - the subject line
        * attachments

        Inheriting classes should raise RequestParseError if the inbound request
        cannot be converted successfully.

        """
        raise NotImplementedError('Must be implemented by inheriting class.')