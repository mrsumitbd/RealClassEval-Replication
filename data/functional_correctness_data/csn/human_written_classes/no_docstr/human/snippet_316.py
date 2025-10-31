from django.contrib.auth.models import AnonymousUser
from account.conf import settings
from account.languages import DEFAULT_LANGUAGE
from django.utils import timezone, translation

class AnonymousAccount:

    def __init__(self, request=None):
        self.user = AnonymousUser()
        self.timezone = settings.TIME_ZONE
        if request is None:
            self.language = DEFAULT_LANGUAGE
        else:
            self.language = translation.get_language_from_request(request, check_path=True)

    def __str__(self):
        return 'AnonymousAccount'