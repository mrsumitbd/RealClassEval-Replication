
import json
import os
from typing import Optional, Any
import requests
from requests.auth import HTTPBasicAuth


class MonzoAPI:

    def __init__(self, access_token: Optional[str] = None) -> None:
        self.access_token = access_token
        self.base_url = "https://api.monzo.com"

    @classmethod
    def authorize(cls, client_id: str, client_secret: str, *, save_to_disk: bool = True, redirect_uri: str = 'http://localhost:6600/pymonzo') -> dict:
        auth_url = f"https://auth.monzo.com/?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
        print(
            f"Please visit this URL to authorize the application: {auth_url}")
        code = input("Enter the authorization code from the URL: ")

        token_url = "https://api.monzo.com/oauth2/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": code
        }
        response = requests.post(token_url, data=data)
        response.raise_for_status()
        token = response.json()

        if save_to_disk:
            with open("monzo_token.json", "w") as f:
                json.dump(token, f)

        return token

    def _update_token(self, token: dict, **kwargs: Any) -> None:
        self.access_token = token.get("access_token")
        self.refresh_token = token.get("refresh_token")
        self.expires_in = token.get("expires_in")
        self.token_type = token.get("token_type")
        self.user_id = token.get("user_id")
