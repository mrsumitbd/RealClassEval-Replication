
import os
import json
import threading
import webbrowser
from typing import Optional, Any
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import requests


class NoSettingsFile(Exception):
    pass


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
    SETTINGS_FILE = os.path.expanduser("~/.monzo_api_settings.json")
    TOKEN_URL = "https://api.monzo.com/oauth2/token"
    AUTH_URL = "https://auth.monzo.com/"

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
        if access_token is not None:
            self.access_token = access_token
            self.token = {"access_token": access_token}
            self.settings = {}
        else:
            if not os.path.exists(self.SETTINGS_FILE):
                raise NoSettingsFile(
                    "Settings file not found and no access_token provided.")
            with open(self.SETTINGS_FILE, "r") as f:
                self.settings = json.load(f)
            if "access_token" not in self.settings:
                raise NoSettingsFile("No access_token in settings file.")
            self.access_token = self.settings["access_token"]
            self.token = self.settings

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
        # Step 1: Get authorization code
        state = "pymonzo_state"
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
        }
        auth_url = cls.AUTH_URL + "?" + \
            "&".join(f"{k}={requests.utils.quote(str(v))}" for k,
                     v in params.items())

        code_holder = {}

        class OAuthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urlparse(self.path)
                qs = parse_qs(parsed.query)
                if "code" in qs and "state" in qs and qs["state"][0] == state:
                    code_holder["code"] = qs["code"][0]
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(
                        b"<html><body><h1>Authorization successful. You can close this window.</h1></body></html>")
                else:
                    self.send_response(400)
                    self.end_headers()

            def log_message(self, format, *args):
                return

        server = HTTPServer(("localhost", 6600), OAuthHandler)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()

        webbrowser.open(auth_url)
        print(f"Please authorize the application in your browser: {auth_url}")

        # Wait for code
        while "code" not in code_holder:
            pass
        server.shutdown()
        code = code_holder["code"]

        # Step 2: Exchange code for token
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code,
        }
        resp = requests.post(cls.TOKEN_URL, data=data)
        resp.raise_for_status()
        token = resp.json()
        token["client_id"] = client_id
        token["client_secret"] = client_secret
        token["redirect_uri"] = redirect_uri

        if save_to_disk:
            with open(cls.SETTINGS_FILE, "w") as f:
                json.dump(token, f)

        return token

    def _update_token(self, token: dict, **kwargs: Any) -> None:
        '''Update settings with refreshed access token and save it to disk.
        Arguments:
            token: OAuth access token.
            **kwargs: Extra kwargs.
        '''
        self.token.update(token)
        self.access_token = self.token.get("access_token")
        self.settings.update(self.token)
        with open(self.SETTINGS_FILE, "w") as f:
            json.dump(self.settings, f)
