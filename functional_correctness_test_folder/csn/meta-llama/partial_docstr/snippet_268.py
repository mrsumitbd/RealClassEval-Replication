
import requests
from typing import Optional, Any, Dict
import json
import os


class NoSettingsFile(Exception):
    pass


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
    SETTINGS_FILE = 'monzo_settings.json'

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
        if access_token is None:
            try:
                with open(self.SETTINGS_FILE, 'r') as f:
                    settings = json.load(f)
                    self.access_token = settings['access_token']
                    self.refresh_token = settings['refresh_token']
                    self.client_id = settings['client_id']
                    self.client_secret = settings['client_secret']
            except FileNotFoundError:
                raise NoSettingsFile("Settings file not found.")
        else:
            self.access_token = access_token

    @classmethod
    def authorize(cls, client_id: str, client_secret: str, *, save_to_disk: bool = True, redirect_uri: str = 'http://localhost:6600/pymonzo') -> Dict:
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
        auth_url = f"https://auth.monzo.com/?response_type=code&redirect_uri={redirect_uri}&client_id={client_id}"
        print(f"Please visit: {auth_url}")

        auth_code = input("Enter the authorization code: ")

        token_url = "https://api.monzo.com/oauth2/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret,
            "redirect_uri": redirect_uri,
            "code": auth_code
        }
        response = requests.post(token_url, headers=headers, data=data)
        token = response.json()

        if save_to_disk:
            with open(cls.SETTINGS_FILE, 'w') as f:
                json.dump({
                    'access_token': token['access_token'],
                    'refresh_token': token['refresh_token'],
                    'client_id': client_id,
                    'client_secret': client_secret
                }, f)

        return token

    def _update_token(self, token: Dict, **kwargs: Any) -> None:
        '''Update settings with refreshed access token and save it to disk.
        Arguments:
            token: OAuth access token.
            **kwargs: Extra kwargs.
        '''
        self.access_token = token['access_token']
        with open(self.SETTINGS_FILE, 'r+') as f:
            settings = json.load(f)
            settings['access_token'] = token['access_token']
            settings['refresh_token'] = token['refresh_token']
            f.seek(0)
            json.dump(settings, f)
            f.truncate()
