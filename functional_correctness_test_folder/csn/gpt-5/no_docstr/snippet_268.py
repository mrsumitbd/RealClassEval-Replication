from __future__ import annotations

import json
import os
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Optional
from urllib.parse import parse_qs, urlparse, urlencode

import requests
import secrets


class MonzoAPI:
    _DEFAULT_TOKEN_PATH = os.path.join(
        os.path.expanduser("~"), ".pymonzo_token.json")
    _AUTH_URL = "https://auth.monzo.com/"
    _TOKEN_URL = "https://api.monzo.com/oauth2/token"

    def __init__(self, access_token: Optional[str] = None) -> None:
        self.token: dict[str, Any] = {}
        self.access_token: Optional[str] = None
        self._token_path = self._DEFAULT_TOKEN_PATH

        if access_token:
            self._update_token(
                {"access_token": access_token, "created_at": int(time.time())})
        else:
            # Attempt to load token from disk
            try:
                if os.path.isfile(self._token_path):
                    with open(self._token_path, "r", encoding="utf-8") as f:
                        token = json.load(f)
                        if isinstance(token, dict) and "access_token" in token:
                            self._update_token(token)
            except Exception:
                pass

    @classmethod
    def authorize(
        cls,
        client_id: str,
        client_secret: str,
        *,
        save_to_disk: bool = True,
        redirect_uri: str = "http://localhost:6600/pymonzo",
    ) -> dict:
        parsed = urlparse(redirect_uri)
        if parsed.scheme != "http" or parsed.hostname not in ("localhost", "127.0.0.1"):
            raise ValueError(
                "redirect_uri must be http://localhost:<port>/<path>")

        state = secrets.token_urlsafe(16)
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
        }
        auth_url = f"{cls._AUTH_URL}?{urlencode(params)}"

        result: dict[str, Any] = {"code": None, "state": None, "error": None}

        class _Handler(BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: Any) -> None:
                return

            def do_GET(self) -> None:
                query = parse_qs(urlparse(self.path).query)
                code = (query.get("code") or [None])[0]
                recv_state = (query.get("state") or [None])[0]
                error = (query.get("error") or [None])[0]

                result["code"] = code
                result["state"] = recv_state
                result["error"] = error

                self.send_response(200 if code and not error else 400)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                if error:
                    self.wfile.write(
                        f"<h1>Authorization failed</h1><p>{error}</p>".encode("utf-8"))
                else:
                    self.wfile.write(
                        b"<h1>Authorization complete</h1><p>You may close this tab.</p>")

        port = parsed.port or 80
        server = HTTPServer((parsed.hostname, port), _Handler)

        server_thread = threading.Thread(
            target=server.serve_forever, daemon=True)
        server_thread.start()

        try:
            webbrowser.open(auth_url)
        except Exception:
            pass

        deadline = time.time() + 300
        try:
            while time.time() < deadline and result["code"] is None and result["error"] is None:
                time.sleep(0.1)
        finally:
            server.shutdown()
            server.server_close()

        if result["error"]:
            raise RuntimeError(f"Authorization error: {result['error']}")
        if result["code"] is None:
            raise TimeoutError(
                "Authorization timed out waiting for redirect with code")
        if result["state"] != state:
            raise RuntimeError("State mismatch during authorization")

        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": result["code"],
        }
        resp = requests.post(cls._TOKEN_URL, data=data, timeout=30)
        resp.raise_for_status()
        token = resp.json()

        # Normalize fields
        if "created_at" not in token:
            token["created_at"] = int(time.time())

        if save_to_disk:
            try:
                with open(cls._DEFAULT_TOKEN_PATH, "w", encoding="utf-8") as f:
                    json.dump(token, f, ensure_ascii=False, indent=2)
            except Exception:
                pass

        return token

    def _update_token(self, token: dict, **kwargs: Any) -> None:
        self.token.update(token or {})
        self.access_token = self.token.get("access_token")

        if "created_at" not in self.token:
            self.token["created_at"] = int(time.time())

        if "expires_in" in self.token and isinstance(self.token["expires_in"], (int, float)):
            try:
                self.token["expires_at"] = int(
                    self.token["created_at"]) + int(self.token["expires_in"])
            except Exception:
                pass

        if kwargs.get("save", False):
            try:
                with open(self._token_path, "w", encoding="utf-8") as f:
                    json.dump(self.token, f, ensure_ascii=False, indent=2)
            except Exception:
                pass
