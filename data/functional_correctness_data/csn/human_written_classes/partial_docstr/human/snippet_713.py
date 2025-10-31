import time
import json
from os.path import expanduser
from os import getenv

class ClientAuth:
    """
    Request authentication and keep access token available through token method. Renew it automatically if necessary

    Args:
        clientId (str): Application clientId delivered by Netatmo on dev.netatmo.com
        clientSecret (str): Application Secret key delivered by Netatmo on dev.netatmo.com
        refreshToken (str) : Scoped refresh token
    """

    def __init__(self, clientId=None, clientSecret=None, refreshToken=None, credentialFile=None):
        clientId = getenv('CLIENT_ID', clientId)
        clientSecret = getenv('CLIENT_SECRET', clientSecret)
        refreshToken = getenv('REFRESH_TOKEN', refreshToken)
        if not (clientId and clientSecret and refreshToken):
            self._credentialFile = credentialFile or expanduser('~/.netatmo.credentials')
            with open(self._credentialFile, 'r', encoding='utf-8') as f:
                cred = {k.upper(): v for k, v in json.loads(f.read()).items()}
        else:
            self._credentialFile = None
        self._clientId = clientId or cred['CLIENT_ID']
        self._clientSecret = clientSecret or cred['CLIENT_SECRET']
        self._accessToken = None
        self.refreshToken = refreshToken or cred['REFRESH_TOKEN']
        self.expiration = 0

    @property
    def accessToken(self):
        if self.expiration < time.time():
            self.renew_token()
        return self._accessToken

    def renew_token(self):
        postParams = {'grant_type': 'refresh_token', 'refresh_token': self.refreshToken, 'client_id': self._clientId, 'client_secret': self._clientSecret}
        resp = postRequest('authentication', _AUTH_REQ, postParams)
        if self.refreshToken != resp['refresh_token']:
            self.refreshToken = resp['refresh_token']
            cred = {'CLIENT_ID': self._clientId, 'CLIENT_SECRET': self._clientSecret, 'REFRESH_TOKEN': self.refreshToken}
            if self._credentialFile:
                with open(self._credentialFile, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(cred, indent=True))
        self._accessToken = resp['access_token']
        self.expiration = int(resp['expire_in'] + time.time())