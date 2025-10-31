
import os
import json
import time
import datetime
import webbrowser
import threading
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Optional, Any, Dict

import requests


class NoSettingsFile(RuntimeError):
    """Raised when the settings file cannot be found and no token was supplied."""
    pass


class MonzoAPI:
    """Monzo public API client.

    To use it, you need to create a new OAuth client in
    https://developers.monzo.com/ and set the redirect URL to
    http://localhost:6600/pymonzo.  The client must be
    confidential if you want automatic token refresh.
    """

    _SETTINGS_FILE = os.path.join(
        os.path.expanduser("~"), ".pymonzo_settings.json")
    _DEFAULT_SCOPES = [
        "account:read",
        "balance:read",
        "transaction:read",
    ]

    def __init__(self, access_token: Optional[str] = None) -> None:
        """Initialize Monzo API client and mount all resources.

        It expects `MonzoAPI.authorize` to be called beforehand, so it can
        load the local settings file containing the API access token.  You
        can also explicitly pass the `access_token`, but it won't be able to
        automatically refresh it once it expires.

        Arguments:
            access_token: OAuth access token.  You can obtain it (and by
                default, save it to disk, so it can refresh automatically)
                by running `MonzoAPI.authorize`.  Alternatively, you can
                get a temporary access token from the Monzo Developer
                Portal.

        Raises:
            NoSettingsFile: When the access token wasn't passed explicitly
                and the settings file couldn't be loaded.
        """
        if access_token is None:
            if not os.path.exists(self._SETTINGS_FILE):
                raise NoSettingsFile(
                    f"Settings file not found: {self._SETTINGS_FILE}"
                )
            with open(self._SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            access_token = data.get("access_token")
            if not access_token:
                raise NoSettingsFile(
                    f"Access token missing in settings file: {self._SETTINGS_FILE}"
                )
            self._token_data = data
        else:
            self._token_data = {"access_token": access_token}

        self.access_token = access_token
        self.session = requests.Session()
        self.session.headers.update(
            {"Authorization": f"Bearer {self.access_token}"}
        )

    @classmethod
    def authorize(
        cls,
        client_id: str,
        client_secret: str,
        *,
        save_to_disk: bool = True,
        redirect_uri: str = "http://localhost:6600/pymonzo",
    ) -> Dict[str, Any]:
        """Use OAuth 2 'Authorization Code Flow' to get Monzo API access token.

        By default, it also saves the token to disk, so it can be loaded
        during `MonzoAPI` initialization.

        Note:
            Monzo API docs: https://docs.monzo.com/#authentication

        Arguments:
            client_id: OAuth client ID.
            client_secret: OAuth client secret.
            save_to_disk: Whether to save the token to disk.
            redirect_uri: Redirect URI specified in OAuth client.

        Returns:
            OAuth token.
        """
        # Build the authorization URL
        auth_params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": " ".join(cls._DEFAULT_SCOPES),
        }
        auth_url = f"https://api.monzo.com/oauth2/authorize?{urllib.parse.urlencode(auth_params)}"

        # Start a local HTTP server to capture the redirect
        code_container = {}

        class _Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urllib.parse.urlparse(self.path)
                qs = urllib.parse.parse_qs(parsed.query)
                if "code" in qs:
                    code_container["code"] = qs["code"][0]
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html")
                    self.end_headers()
                    self.wfile.write(
                        b"<html><body><h1>Authorization successful. You may close this window.</h1></body></html>")
                else:
                    self.send_response(400)
                    self.end_headers()

            def log_message(self, format, *args):
                # Suppress logging
                return

        server_address = ("", 6600)
        httpd = HTTPServer(server_address, _Handler)

        def _run_server():
            httpd.handle_request()

        server_thread = threading.Thread(target=_run_server, daemon=True)
        server_thread.start()

        # Open the browser for the user
        webbrowser.open(auth_url, new=1, autoraise=True)

        # Wait for the code to be captured
        timeout = 120  # seconds
        start = time.time()
        while "code" not in code_container:
            if time.time() - start > timeout:
                httpd.shutdown()
                raise RuntimeError("Authorization timed out.")
            time.sleep(0.1)

        httpd.shutdown()
        code = code_container["code"]

        # Exchange the code for a token
        token_url = "https://api.monzo.com/oauth2/token"
        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        }
        resp = requests.post(token_url, data=token_data)
        resp.raise_for_status()
        token = resp.json()

        # Save to disk if requested
        if save_to_disk:
            settings = {
                "access_token": token["access_token"],
                "refresh_token": token.get("refresh_token"),
                "expires_at": token
