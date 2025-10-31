
import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from typing import Optional, Any, Dict
import json
import os


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

    SETTINGS_FILE = 'monzo_settings.json'

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
        if access_token is None:
            try:
                with open(self.SETTINGS_FILE, 'r') as f:
                    self.settings = json.load(f)
                    self.access_token = self.settings['access_token']
            except FileNotFoundError:
                raise NoSettingsFile("Settings file not found.")
        else:
            self.access_token = access_token

    @classmethod
    def authorize(cls, client_id: str, client_secret: str, *, save_to_disk: bool = True, redirect_uri: str = 'http://localhost:6600/pymonzo') -> Dict:
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
        auth_url = f"https://auth.monzo.com/?response_type=code&redirect_uri={redirect_uri}&client_id={client_id}"
        webbrowser.open(auth_url)

        class RequestHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed_path = urlparse(self.path)
                code = parse_qs(parsed_path.query)['code'][0]
                token = cls._get_token(
                    code, client_id, client_secret, redirect_uri)
                if save_to_disk:
                    with open(cls.SETTINGS_FILE, 'w') as f:
                        json.dump(token, f)
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(
                    b"Authorization successful. You can now close this window.")

        server = HTTPServer(('localhost', 6600), RequestHandler)
        server.handle_request()
        with open(cls.SETTINGS_FILE, 'r') as f:
            return json.load(f)

    @classmethod
    def _get_token(cls, code: str, client_id: str, client_secret: str, redirect_uri: str) -> Dict:
        token_url = "https://api.monzo.com/oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'code': code
        }
        response = requests.post(token_url, headers=headers, data=data)
        return response.json()

    def _update_token(self, token: Dict, **kwargs: Any) -> None:
        '''Update settings with refreshed access token and save it to disk.
        Arguments:
            token: OAuth access token.
            **kwargs: Extra kwargs.
        '''
        self.settings['access_token'] = token['access_token']
        with open(self.SETTINGS_FILE, 'w') as f:
            json.dump(self.settings, f)


class NoSettingsFile(Exception):
    pass
