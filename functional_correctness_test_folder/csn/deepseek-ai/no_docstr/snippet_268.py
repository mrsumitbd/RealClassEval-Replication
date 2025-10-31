
from typing import Optional, Any, Dict
import requests
from requests.auth import HTTPBasicAuth
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os


class MonzoAPI:

    def __init__(self, access_token: Optional[str] = None) -> None:
        self.access_token = access_token
        self.base_url = "https://api.monzo.com"

    @classmethod
    def authorize(
        cls,
        client_id: str,
        client_secret: str,
        *,
        save_to_disk: bool = True,
        redirect_uri: str = 'http://localhost:6600/pymonzo'
    ) -> Dict:
        auth_url = (
            f"https://auth.monzo.com/?client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            "&response_type=code"
        )

        class AuthHandler(BaseHTTPRequestHandler):
            def do_GET(self):
                query = urlparse(self.path).query
                params = parse_qs(query)
                if 'code' in params:
                    self.server.auth_code = params['code'][0]
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(
                        b"Authorization successful! You can close this window.")
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b"Authorization failed.")

        server_address = ('localhost', 6600)
        httpd = HTTPServer(server_address, AuthHandler)
        webbrowser.open(auth_url)
        httpd.handle_request()

        auth_code = httpd.auth_code

        token_url = "https://api.monzo.com/oauth2/token"
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'code': auth_code
        }

        response = requests.post(token_url, data=data)
        token_data = response.json()

        if save_to_disk:
            with open('monzo_token.json', 'w') as f:
                json.dump(token_data, f)

        return token_data

    def _update_token(self, token: Dict, **kwargs: Any) -> None:
        if self.access_token is None:
            self.access_token = token.get('access_token')
        if kwargs.get('save_to_disk', False):
            with open('monzo_token.json', 'w') as f:
                json.dump(token, f)
