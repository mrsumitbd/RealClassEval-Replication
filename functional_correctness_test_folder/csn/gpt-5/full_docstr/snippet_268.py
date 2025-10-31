from __future__ import annotations

import json
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Optional, Tuple
from urllib.parse import urlparse, parse_qs, urlencode

import requests


class NoSettingsFile(FileNotFoundError):
    pass


class _AuthCodeServer(HTTPServer):
    def __init__(self, server_address: Tuple[str, int], RequestHandlerClass: type[BaseHTTPRequestHandler]) -> None:
        super().__init__(server_address, RequestHandlerClass)
        self.code: Optional[str] = None
        self.state: Optional[str] = None
        self.error: Optional[str] = None


class _AuthCodeHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        code = params.get("code", [None])[0]
        state = params.get("state", [None])[0]
        error = params.get("error", [None])[0]

        assert isinstance(self.server, _AuthCodeServer)
        self.server.code = code
        self.server.state = state
        self.server.error = error

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        body = (
            "<html><head><title>Monzo Auth</title></head>"
            "<body><h2>Authorization complete</h2>"
            "<p>You can close this window.</p></body></html>"
        )
        self.wfile.write(body.encode("utf-8"))

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return


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

    AUTH_URL = "https://auth.monzo.com/"
    TOKEN_URL = "https://api.monzo.com/oauth2/token"
    SETTINGS_PATH = Path.home() / ".pymonzo.json"

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
        self.settings: dict[str, Any] = {}

        if access_token:
            self.access_token = access_token
            self.session.headers.update(
                {"Authorization": f"Bearer {self.access_token}"})
            return

        self.settings = self._load_settings()
        token = self.settings.get("token")
        if not token or "access_token" not in token:
            raise NoSettingsFile("No access token available in settings file.")

        self.access_token = token["access_token"]
        self.session.headers.update(
            {"Authorization": f"Bearer {self.access_token}"})

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
                "redirect_uri must include explicit host and port, e.g., http://localhost:6600/pymonzo")

        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
        }
        auth_url = f"{cls.AUTH_URL}?{urlencode(params)}"

        server = _AuthCodeServer(
            (parsed.hostname, parsed.port), _AuthCodeHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            webbrowser.open(auth_url)
            code = cls._wait_for_code(server, timeout=300)
        finally:
            server.shutdown()
            server.server_close()

        if server.error:
            raise RuntimeError(f"Authorization error: {server.error}")
        if not code:
            raise TimeoutError("Timed out waiting for authorization code.")

        token = cls._exchange_code_for_token(
            code=code,
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=redirect_uri,
        )

        if save_to_disk:
            settings = {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "token_url": cls.TOKEN_URL,
                "token": token,
            }
            cls._save_settings(settings)

        return token

    def _update_token(self, token: dict, **kwargs: Any) -> None:
        '''Update settings with refreshed access token and save it to disk.
        Arguments:
            token: OAuth access token.
            **kwargs: Extra kwargs.
        '''
        settings = self._load_settings()
        token = dict(token)
        if "expires_in" in token and "expires_at" not in token:
            token["expires_at"] = int(time.time()) + int(token["expires_in"])
        settings["token"] = token
        self._save_settings(settings)
        self.access_token = token.get("access_token", self.access_token)
        self.session.headers.update(
            {"Authorization": f"Bearer {self.access_token}"})

    @staticmethod
    def _wait_for_code(server: _AuthCodeServer, timeout: int = 300) -> Optional[str]:
        deadline = time.time() + timeout
        while time.time() < deadline:
            if server.code or server.error:
                return server.code
            time.sleep(0.1)
        return None

    @classmethod
    def _exchange_code_for_token(
        cls,
        *,
        code: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
    ) -> dict:
        resp = requests.post(
            cls.TOKEN_URL,
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uri": redirect_uri,
                "code": code,
            },
            timeout=30,
        )
        resp.raise_for_status()
        token = resp.json()
        if "expires_in" in token and "expires_at" not in token:
            token["expires_at"] = int(time.time()) + int(token["expires_in"])
        return token

    @classmethod
    def _load_settings(cls) -> dict:
        path = cls.SETTINGS_PATH
        if not path.exists():
            raise NoSettingsFile(f"Settings file not found: {path}")
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)

    @classmethod
    def _save_settings(cls, settings: dict) -> None:
        path = cls.SETTINGS_PATH
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = path.with_suffix(path.suffix + ".tmp")
        with tmp.open("w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, sort_keys=True)
        tmp.replace(path)
