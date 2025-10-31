import requests

class Firebase:
    """ Firebase Interface """

    def __init__(self, config):
        self.api_key = config['apiKey']
        self.auth_domain = config['authDomain']
        self.database_url = config['databaseURL']
        self.storage_bucket = config['storageBucket']
        self.credentials = None
        self.requests = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=3)
        for scheme in ('http://', 'https://'):
            self.requests.mount(scheme, adapter)

    def auth(self):
        return Auth(self.api_key, self.requests, self.credentials)

    def database(self):
        return Database(self.credentials, self.api_key, self.database_url, self.requests)