class TokenBase:
    __slots__ = ()

    def __call__(self, request, refresh_token=False):
        raise NotImplementedError('Subclasses must implement this method.')

    def validate_request(self, request):
        """
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """
        raise NotImplementedError('Subclasses must implement this method.')

    def estimate_type(self, request):
        """
        :param request: OAuthlib request.
        :type request: oauthlib.common.Request
        """
        raise NotImplementedError('Subclasses must implement this method.')