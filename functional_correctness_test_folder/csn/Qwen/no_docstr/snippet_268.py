
from typing import Optional, Any, Dict
import requests


class MonzoAPI:

    def __init__(self, access_token: Optional[str] = None) -> None:
        self.access_token = access_token

    @classmethod
    def authorize(cls, client_id: str, client_secret: str, *, save_to_disk: bool = True, redirect_uri: str = 'http://localhost:6600/pymonzo') -> Dict[str, Any]:
        auth_url = "https://auth.monzo.com"
        token_url = "https://api.monzo.com/oauth2/token"
        params = {
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'state': 'some_random_state'
        }
        print(f"Please go to {auth_url} and authorize the app.")
        auth_code = input("Enter the code you received: ")
        data = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'code': auth_code
        }
        response = requests.post(token_url, data=data)
        token = response.json()
        if save_to_disk:
            with open('monzo_token.json', 'w') as f:
                import json
                json.dump(token, f)
        return token

    def _update_token(self, token: Dict[str, Any], **kwargs: Any) -> None:
        self.access_token = token.get('access_token')
        if kwargs.get('save_to_disk', False):
            with open('monzo_token.json', 'w') as f:
                import json
                json.dump(token, f)
