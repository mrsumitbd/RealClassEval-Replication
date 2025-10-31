from tweepy.errors import TweepyException
import requests

class OAuth2AppHandler:
    """OAuth 2.0 Bearer Token (App-Only) using API / Consumer key and secret
    authentication handler

    .. versionchanged:: 4.5
        Renamed from :class:`AppAuthHandler`
    """

    def __init__(self, consumer_key, consumer_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self._bearer_token = ''
        resp = requests.post('https://api.twitter.com/oauth2/token', auth=(self.consumer_key, self.consumer_secret), data={'grant_type': 'client_credentials'})
        data = resp.json()
        if data.get('token_type') != 'bearer':
            raise TweepyException(f"""Expected token_type to equal "bearer", but got {data.get('token_type')} instead""")
        self._bearer_token = data['access_token']

    def apply_auth(self):
        return OAuth2BearerHandler(self._bearer_token)