import json
from six.moves import urllib, http_cookiejar

class GalaxySqnLimsApi:
    """Manage talking with the Galaxy REST api for sequencing information.
    """

    def __init__(self, base_url, user, passwd):
        self._base_url = base_url
        cj = http_cookiejar.LWPCookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)
        login = dict(email=user, password=passwd, login_button='Login')
        req = urllib.request.Request('%s/user/login' % self._base_url, urllib.parse.urlencode(login))
        response = urllib.request.urlopen(req)

    def run_details(self, run):
        """Retrieve sequencing run details as a dictionary.
        """
        run_data = dict(run=run)
        req = urllib.request.Request('%s/nglims/api_run_details' % self._base_url, urllib.parse.urlencode(run_data))
        response = urllib.request.urlopen(req)
        info = json.loads(response.read())
        if 'error' in info:
            raise ValueError('Problem retrieving info: %s' % info['error'])
        else:
            return info['details']