class _WithLanguageMixin:

    @property
    def language(self):
        return self.related('languageReference')

    @property
    def languages(self):
        return self.all_related('languageReference')