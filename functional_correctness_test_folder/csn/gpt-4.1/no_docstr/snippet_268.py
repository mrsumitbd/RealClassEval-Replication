
from typing import Optional, Any, Dict
import os
import json
import webbrowser
import http.server
import socketserver
import threading
import urllib.parse
import requests


class MonzoAPI:
    TOKEN_FILE = os.path.expanduser("~/.monzo_token.json")
    AUTH_URL = "https://auth.monzo.com/"
    TOKEN_URL = "https://api.monzo.com/oauth2/token"

    def __init__(self, access_token: Optional[str] = None) -> None:
        self.token: Optional[dict] = None
        self.access_token: Optional[str] = access_token
        if access_token is None:
            if os.path.exists(self.TOKEN_FILE):
                with open(self.TOKEN_FILE, "r") as f:
                    self.token = json.load(f)
                    self.access_token = self.token.get("access_token")

    @classmethod
    def authorize(cls, client_id: str, client_secret: str, *, save_to_disk: bool = True, redirect_uri: str = 'http://localhost:6600/pymonzo') -> dict:
        state = "monzo_state"
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "state": state,
        }
        url = cls.AUTH_URL + "?" + urllib.parse.urlencode(params)
        code_holder = {}

        class Handler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                parsed = urllib.parse.urlparse(self.path)
                qs = urllib.parse.parse_qs(parsed.query)
                if "code" in qs:
                    code_holder["code"] = qs["code"][0]
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(
                        b"Authorization successful. You can close this window.")
                else:
                    self.send_response(400)
                    self.end_headers()

            def log_message(self, format, *args):
                return

        server = socketserver.TCPServer(("localhost", 6600), Handler)
        thread = threading.Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()

        webbrowser.open(url)
        while "code" not in code_holder:
            pass
        server.shutdown()
        server.server_close()
        code = code_holder["code"]

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
        if save_to_disk:
            with open(cls.TOKEN_FILE, "w") as f:
                json.dump(token, f)
        return token

    def _update_token(self, token: dict, **kwargs: Any) -> None:
        self.token = token
        self.access_token = token.get("access_token")
        if kwargs.get("save_to_disk", True):
            with open(self.TOKEN_FILE, "w") as f:
                json.dump(token, f)
