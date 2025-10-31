
import requests
from typing import Optional, Any, Dict
import webbrowser
import http.server
import urllib.parse
import json
import os


class MonzoAPI:

    def __init__(self, access_token: Optional[str] = None) -> None:
        self.access_token = access_token
        self.client_id = None
        self.client_secret = None

    @classmethod
    def authorize(cls, client_id: str, client_secret: str, *, save_to_disk: bool = True, redirect_uri: str = 'http://localhost:6600/pymonzo') -> Dict:
        class RequestHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                parsed_path = urllib.parse.urlparse(self.path)
                query = urllib.parse.parse_qs(parsed_path.query)
                if 'code' in query:
                    self.server.authorization_code = query['code'][0]
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(
                        b'Authorization successful. You can close this tab now.')
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(b'Authorization failed.')

        server = http.server.HTTPServer(('localhost', 6600), RequestHandler)
        server.authorization_code = None

        auth_url = f'https://auth.monzo.com/?response_type=code&redirect_uri={redirect_uri}&client_id={client_id}'
        webbrowser.open(auth_url)

        while server.authorization_code is None:
            server.handle_request()

        token_url = 'https://api.monzo.com/oauth2/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'code': server.authorization_code
        }
        response = requests.post(token_url, headers=headers, data=data)
        token = response.json()

        if save_to_disk:
            with open('token.json', 'w') as f:
                json.dump(token, f)

        return token

    def _update_token(self, token: Dict, **kwargs: Any) -> None:
        if 'access_token' in token:
            self.access_token = token['access_token']
        if 'client_id' in kwargs:
            self.client_id = kwargs['client_id']
        if 'client_secret' in kwargs:
            self.client_secret = kwargs['client_secret']
