
import os
import json
import time
import uuid
from typing import Optional, Any, Dict

import requests


class MonzoAPI:
    """
    A minimal wrapper around the Monzo OAuth2 flow and token handling.
    """

    TOKEN_FILE = os.path.expanduser("~/.pymonzo/token.json")
    AUTH_URL = "https://api.monzo.com/oauth2/authorize"
    TOKEN_URL = "https://api.monzo.com/oauth2/token"
    DEFAULT_SCOPES = [
        "account:read",
        "transaction:read",
        "card:read",
    ]

    def __init__(self, access_token: Optional[str] = None) -> None:
        """
        Initialise the API client.

        If an access_token is supplied it will be used directly.
        Otherwise the client will attempt to load a token from disk.
        """
        self.access_token: Optional[str] = access_token
        self.refresh_token: Optional[str] = None
        self.expires_at: Optional[int] = None
        self.token: Optional[Dict[str, Any]] = None

        if not self.access_token:
            self._load_token_from_disk()

        if not self.access_token:
            raise ValueError(
                "No access token supplied and no token found on disk. "
                "Please run MonzoAPI.authorize() first."
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
        """
        Perform the OAuth2 authorization flow.

        The user is prompted to visit a URL and paste the resulting
        authorization code. The code is exchanged for an access token
        which is returned as a dictionary. If `save_to_disk` is True
        the token is persisted to ~/.pymonzo/token.json.
        """
        # Build the authorization URL
        state = uuid.uuid4().hex
        params = {
            "client_id": client_id,
            "response_type": "code",
            "redirect_uri": redirect_uri,
            "scope": " ".join(cls.DEFAULT_SCOPES),
            "state": state,
        }
        auth_url = f"{cls.AUTH_URL}?{requests.compat.urlencode(params)}"

        print("Please visit the following URL to authorize the application:")
        print(auth_url)
        print("\nAfter authorising, you will be redirected to a URL similar to:")
        print(f"{redirect_uri}?code=YOUR_CODE&state={state}")
        print("\nPaste the 'code' parameter value below:")

        code = input("Authorization code: ").strip()
        if not code:
            raise ValueError("No authorization code provided.")

        # Exchange the code for a token
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
        }
        response = requests.post(cls.TOKEN_URL, data=data)
        if response.status_code != 200:
            raise RuntimeError(
                f"Token request failed: {response.status_code} {response.text}"
            )
        token = response.json()

        # Persist token if requested
        if save_to_disk:
            cls._save_token_to_disk_static(token)

        return token

    def _update_token(self, token: Dict[str, Any], **kwargs: Any) -> None:
        """
        Update the client's token information.

        Parameters
        ----------
        token : dict
            The token dictionary returned by the Monzo API.
        kwargs : dict
            Optional keyword arguments. Supported keys:
                - save_to_disk (bool): whether to persist the token.
        """
        self.access_token = token.get("access_token")
        self.refresh_token = token.get("refresh_token")
        self.expires_at = token.get("expires_at")
        self.token = token

        if kwargs.get("save_to_disk", False):
            self._save_token_to_disk()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _load_token_from_disk(self) -> None:
        """Load token from the default token file."""
        if not os.path.exists(self.TOKEN_FILE):
            return

        try:
            with open(self.TOKEN_FILE, "r", encoding="utf-8") as f:
                token = json.load(f)
        except Exception:
            return

        self.access_token = token.get("access_token")
        self.refresh_token = token.get("refresh_token")
        self.expires_at = token.get("expires_at")
        self.token = token

    def _save_token
