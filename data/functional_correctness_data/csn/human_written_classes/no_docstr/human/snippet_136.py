import os
import datetime
from http.client import HTTPConnection

class Client:
    DEFAULT_ENDPOINT = 'http://localhost:8080'

    def __init__(self, endpoint=None, key=None, secret=None, token=None, username=None, password=None, timeout=5.0, ssl_verify=True, headers=None, debug=False):
        self.endpoint = endpoint or os.environ.get('ALERTA_ENDPOINT', self.DEFAULT_ENDPOINT)
        if debug:
            HTTPConnection.debuglevel = 1
        key = key or os.environ.get('ALERTA_API_KEY', '')
        self.http = HTTPClient(self.endpoint, key, secret, token, username, password, timeout, ssl_verify, headers, debug)

    def send_alert(self, resource, event, **kwargs):
        data = {'id': kwargs.get('id'), 'resource': resource, 'event': event, 'environment': kwargs.get('environment'), 'severity': kwargs.get('severity'), 'correlate': kwargs.get('correlate', None) or list(), 'service': kwargs.get('service', None) or list(), 'group': kwargs.get('group'), 'value': kwargs.get('value'), 'text': kwargs.get('text'), 'tags': kwargs.get('tags', None) or list(), 'attributes': kwargs.get('attributes', None) or dict(), 'origin': kwargs.get('origin'), 'type': kwargs.get('type'), 'createTime': datetime.datetime.utcnow(), 'timeout': kwargs.get('timeout'), 'rawData': kwargs.get('raw_data'), 'customer': kwargs.get('customer')}
        return self.http.post('/alert', data)

    def action(self, id, action, text='', timeout=None):
        data = {'action': action, 'text': text, 'timeout': timeout}
        return self.http.put(f'/alert/{id}/action', data)

    def delete_alert(self, id):
        return self.http.delete(f'/alert/{id}')