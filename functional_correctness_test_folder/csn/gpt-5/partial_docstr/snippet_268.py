import json
import os
import threading
import time
import secrets
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional, Any
from urllib.parse import urlparse, parse_qs, urlencode

import requests


class NoSettingsFile(FileNotFoundError):
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

    SETTINGS_PATH = os.path.join(os.path.expanduser("~"), ".pymonzo.json")
    AUTH_URL = "https://auth.monzo.com/"
    TOKEN_URL = "https://api.monzo.com/oauth2/token"

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
        self.session = requests.Session()
        self.settings = {}

        if access_token:
            self.token = {"access_token": access_token}
            self.session.headers.update(
                {"Authorization": f"Bearer {access_token}"})
            return

        if not os.path.exists(self.SETTINGS_PATH):
            raise NoSettingsFile(
                f"Settings file not found at {self.SETTINGS_PATH}")

        try:
            with open(self.SETTINGS_PATH, "r", encoding="utf-8") as f:
                self.settings = json.load(f)
        except Exception as e:
            raise NoSettingsFile(f"Unable to load settings file: {e}") from e

        token = self.settings.get("token", {})
        if not token or "access_token" not in token:
            raise NoSettingsFile("Access token not found in settings file")

        self.token = token
        self.session.headers.update(
            {"Authorization": f"Bearer {token['access_token']}"})

    @classmethod
    def authorize(
        cls,
        client_id: str,
        client_secret: str,
        *,
        save_to_disk: bool = True,
        redirect_uri: str = "http://localhost:6600/pymonzo",
    ) -> dict:
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

        parsed = urlparse(redirect_uri)
        if parsed.hostname is None or parsed.port is None:
            raise ValueError(
                "redirect_uri must include explicit hostname and port, e.g. http://localhost:6600/pymonzo")

        state = secrets.token_urlsafe(24)
        query = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
        }
        auth_url = f"{cls.AUTH_URL}?{urlencode(query)}"

        code_holder = {"code": None, "state": None, "error": None}

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                try:
                    q = parse_qs(urlparse(self.path).query)
                    code = q.get("code", [None])[0]
                    recv_state = q.get("state", [None])[0]
                    error = q.get("error", [None])[0]
                    code_holder["code"] = code
                    code_holder["state"] = recv_state
                    code_holder["error"] = error
                    self.send_response(200)
                    self.send_header(
                        "Content-Type", "text/html; charset=utf-8")
                    self.end_headers()
                    if error:
                        self.wfile.write(
                            b"<html><body><h3>Authorization failed.</h3>You can close this window.</body></html>")
                    else:
                        self.wfile.write(
                            b"<html><body><h3>Authorization successful.</h3>You can close this window.</body></html>")
                except Exception:
                    self.send_response(500)
                    self.end_headers()

            def log_message(self, fmt, *args):
                return

        server = HTTPServer((parsed.hostname, parsed.port), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()

        try:
            webbrowser.open(auth_url)
        except Exception:
            pass

        timeout = time.time() + 300
        while time.time() < timeout and code_holder["code"] is None and code_holder["error"] is None:
            time.sleep(0.1)

        server.shutdown()
        thread.join(timeout=2)

        if code_holder["error"]:
            raise RuntimeError(f"Authorization failed: {code_holder['error']}")
        if code_holder["code"] is None:
            raise TimeoutError("Timed out waiting for authorization code")

        if code_holder["state"] != state:
            raise RuntimeError("State mismatch during OAuth flow")

        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code_holder["code"],
        }
        resp = requests.post(cls.TOKEN_URL, data=data, timeout=30)
        resp.raise_for_status()
        token = resp.json()

        if save_to_disk:
            settings = {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "token": token,
                "saved_at": int(time.time()),
            }
            with open(cls.SETTINGS_PATH, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=2, sort_keys=True)

        return token

    def _update_token(self, token: dict, **kwargs: Any) -> None:
        '''Update settings with refreshed access token and save it to disk.
        Arguments:
            token: OAuth access token.
            **kwargs: Extra kwargs.
        '''
        self.token = token
        self.session.headers.update(
            {"Authorization": f"Bearer {token.get('access_token', '')}"})

        if not os.path.exists(self.SETTINGS_PATH):
            return

        try:
            with open(self.SETTINGS_PATH, "r", encoding="utf-8") as f:
                settings = json.load(f)
        except Exception:
            settings = {}

        settings["token"] = token
        settings["updated_at"] = int(time.time())

        if kwargs:
            settings.setdefault("meta", {}).update(kwargs)

        with open(self.SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, sort_keys=True)
