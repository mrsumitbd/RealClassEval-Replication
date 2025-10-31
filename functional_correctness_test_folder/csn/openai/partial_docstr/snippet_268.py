
import os
import json
import time
import datetime
import webbrowser
import urllib.parse
import http.server
import socketserver
import threading
from typing import Optional, Any, Dict

import requests

# --------------------------------------------------------------------------- #
# Exceptions
# --------------------------------------------------------------------------- #


class NoSettingsFile(Exception):
    """Raised when the settings file cannot be found and no token was supplied."""
    pass


# --------------------------------------------------------------------------- #
# MonzoAPI
# --------------------------------------------------------------------------- #
class MonzoAPI:
    """Monzo public API client.

    To use it, you need to create a new OAuth client in
    https://developers.monzo.com/ and set the redirect URL to
    http://localhost:6600/pymonzo.  The client must be
    confidential if you want automatic token refresh.

    The access token is stored in a JSON file under
    ~/.pymonzo/settings.json by default.
    """

    _SETTINGS_DIR = os.path.join(os.path.expanduser("~"), ".pymonzo")
    _SETTINGS_FILE = os.path.join(_SETTINGS_DIR, "settings.json")
    _AUTH_URL = "https://api.monzo.com/oauth2/authorize"
    _TOKEN_URL = "https://api.monzo.com/oauth2/token"
    _API_BASE = "https://api.monzo.com"

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
                get a temporary access token from the Monzo Developer Portal.

        Raises:
            NoSettingsFile: When the access token wasn't passed explicitly and
                the settings file couldn't be loaded.
        """
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

        if access_token:
            self.access_token = access_token
            self.session.headers.update(
                {"Authorization": f"Bearer {self.access_token}"})
            self._token_data = {"access_token": access_token}
        else:
            self._load_settings()

        # If we have a full token dict, try to refresh if needed
        if isinstance(self._token_data, dict):
            self._maybe_refresh_token()

    # ----------------------------------------------------------------------- #
    # Authorization
    # ----------------------------------------------------------------------- #
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

        By default, it also saves the token to disk, so it can be loaded during
        `MonzoAPI` initialization.

        Note:
            Monzo API docs: https://docs.monzo.com/#authentication

        Arguments:
            client_id: OAuth client ID.
            client_secret: OAuth client secret.
            save_to_disk: Whether to save the token to disk.
            redirect_uri: Redirect URI specified in OAuth client.

        Returns:
            OAuth token dict.
        """
        # Build the authorization URL
        params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": "account:read balance:read transaction:read",
            "state": "pymonzo",
        }
        auth_url = f"{cls._AUTH_URL}?{urllib.parse.urlencode(params)}"

        # Start a simple HTTP server to capture the redirect
        code_container = {}

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urllib.parse.urlparse(self.path)
                qs = urllib.parse.parse_qs(parsed.query)
                if "code" in qs:
                    code_container["code"] = qs["code"][0]
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(
                        b"<html><body><h1>Authorization successful. You may close this window.</h1></body></html>")
                else:
                    self.send_response(400)
                    self.end_headers()

            def log_message(self, format, *args):
                # Suppress logging
                return

        httpd = socketserver.TCPServer(("localhost", 6600), Handler)
        thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        thread.start()

        # Open the browser
        webbrowser.open(auth_url)

        # Wait until we get the code or timeout
        timeout = 120
        start = time.time()
        while "code" not in code_container and time.time() - start < timeout:
            time.sleep(0.5)

        httpd.shutdown()
        thread.join()

        if "code" not in code_container:
            raise RuntimeError("Authorization timed out or failed.")

        code = code_container["code"]

        # Exchange code for token
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
        }
        resp = requests.post(cls._TOKEN_URL, data=data)
        resp.raise_for_status()
        token = resp.json()

        # Compute expires_at
        if "expires_in" in token:
            token["expires_at"] = int(time.time()) + int(token["expires_in"])

        if save_to_disk:
            cls._save_settings(token)

        return token

    # ----------------------------------------------------------------------- #
    # Token handling
    # ----------------------------------------------------------------------- #
    def _maybe_refresh_token(self) -> None:
        """Refresh the access token if it has expired."""
        token = self._token_data
        if not isinstance(token, dict):
            return
        expires_at = token.get("expires_at")
        if expires_at and time.time() > expires_at - 60:  # refresh 1 minute before expiry
            self._refresh_token()

    def _refresh_token(self) -> None:
        """Refresh the access token using the refresh token."""
        token = self._token_data
        if not isinstance(token, dict) or "refresh_token" not in token:
            raise RuntimeError("No refresh token available.")
        data = {
            "client_id": token.get("client_id"),
            "client_secret": token.get("client_secret"),
            "grant_type": "refresh_token",
            "refresh_token": token["refresh_token"],
        }
        resp = requests.post(self._TOKEN_URL, data=data)
        resp.raise_for_status()
        new_token = resp.json()
        if "expires_in" in new_token:
            new_token["expires_at"] = int(
                time.time()) + int(new_token["expires_in"])
        # Preserve client_id and client_secret if present
        new_token.setdefault("client_id", token.get("client_id"))
        new_token.setdefault("client_secret", token.get("client_secret"))
        self._update_token(new_token)

    def _update_token(self, token: Dict[str, Any], **kwargs: Any) -> None:
        """Update settings with refreshed access token and save it to disk.

        Arguments:
            token: OAuth access token.
            **kwargs: Extra kwargs.
        """
        self.access_token = token["access_token"]
        self.session.headers.update(
            {"Authorization": f"Bearer {self.access_token}"})
        self._token
