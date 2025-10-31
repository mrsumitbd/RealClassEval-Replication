
import os
import json
import webbrowser
from typing import Optional, Any
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import requests


class MonzoAPI:
    '''Monzo public API client.
    To use it, you need to create a new OAuth client in [Monzo Developer Portal].
    The `Redirect URLs` should be set to `http://localhost:6600/pymonzo` and
    `Confidentiality` should be set to `Confidential` if you'd like to automatically
    refresh the access token when it expires.
    You can now use `Client ID` and `Client secret` in [`pymonzo.MonzoAPI.authorize`][]
    to finish the OAuth 2 'Authorization Code Flow' and get the API access token
    (which is by default saved to disk and refreshed when expired).
    [Monzo Developer Portal]: https://developers.monzo.com/
    Note:
        Monzo API docs: https://docs.monzo.com/
    '''

    def __init__(self, access_token: Optional[str] = None) -> None:
        '''Initialize Monzo API client and mount all resources.
        It expects [`pymonzo.MonzoAPI.authorize`][] to be called beforehand, so
        it can load the local settings file containing the API access token. You
        can also explicitly pass the `access_token`, but it won't be able to
        automatically refresh it once it expires.
        Arguments:
            access_token: OAuth access token. You can obtain it (and by default, save
                it to disk, so it can refresh automatically) by running
                [`pymonzo.MonzoAPI.authorize`][]. Alternatively, you can get a
                temporary access token from the [Monzo Developer Portal].
                [Monzo Developer Portal]: https://developers.monzo.com/
        Raises:
            NoSettingsFile: When the access token wasn't passed explicitly and the
                settings file couldn't be loaded.
        '''
        self.access_token = access_token
        self.settings_file = os.path.expanduser('~/.pymonzo')
        if not self.access_token:
            try:
                with open(self.settings_file, 'r') as f:
                    self.access_token = json.load(f)['access_token']
            except FileNotFoundError:
                raise NoSettingsFile(
                    "Settings file not found. Please run MonzoAPI.authorize() first.")

    @classmethod
    def authorize(cls, client_id: str, client_secret: str, *, save_to_disk: bool = True, redirect_uri: str = 'http://localhost:6600/pymonzo') -> dict:
        '''Use OAuth 2 'Authorization Code Flow' to get Monzo API access token.
        By default, it also saves the token to disk, so it can be loaded during
        [`pymonzo.MonzoAPI`][] initialization.
        Note:
            Monzo API docs: https://docs.monzo.com/#authentication
        Arguments:
            client_id: OAuth client ID.
            client_secret: OAuth client secret.
            save_to_disk: Whether to save the token to disk.
            redirect_uri: Redirect URI specified in OAuth client.
        Returns:
            OAuth token.
        '''
        auth_url = f'https://auth.monzo.com/?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'
        webbrowser.open(auth_url)

        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(
                    b'<html><head><title>Monzo OAuth</title></head>')
                self.wfile.write(
                    b'<body><h1>You can now close this window.</h1></body></html>')

                query = urlparse(self.path).query
                params = parse_qs(query)
                code = params.get('code', [None])[0]

                if code:
                    token_url = 'https://api.monzo.com/oauth2/token'
                    data = {
                        'grant_type': 'authorization_code',
                        'client_id': client_id,
                        'client_secret': client_secret,
                        'redirect_uri': redirect_uri,
                        'code': code
                    }
                    response = requests.post(token_url, data=data)
                    token = response.json()

                    if save_to_disk:
                        settings_file = os.path.expanduser('~/.pymonzo')
                        with open(settings_file, 'w') as f:
                            json.dump(token, f)

                    self.server.token = token

        server_address = ('', 6600)
        httpd = HTTPServer(server_address, RequestHandler)
        httpd.handle_request()
        return httpd.token

    def _update_token(self, token: dict, **kwargs: Any) -> None:
        '''Update settings with refreshed access token and save it to disk.
        Arguments:
            token: OAuth access token.
            **kwargs: Extra kwargs.
        '''
        with open(self.settings_file, 'w') as f:
            json.dump(token, f)
        self.access_token = token['access_token']


class NoSettingsFile(Exception):
    pass
