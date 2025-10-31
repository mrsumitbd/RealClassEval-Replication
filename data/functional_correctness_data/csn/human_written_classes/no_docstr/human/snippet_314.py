from hashlib import sha256
import hmac
from datetime import datetime

class SigV4Auth:

    def __init__(self, access_key, secret_key, session_token=None, region='us-east-1'):
        self.access_key = access_key
        self.secret_key = secret_key
        self.session_token = session_token
        self.region = region

    def add_auth(self, request):
        timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        request.headers['X-Amz-Date'] = timestamp
        if self.session_token:
            request.headers['X-Amz-Security-Token'] = self.session_token
        canonical_headers = ''.join((f'{k.lower()}:{request.headers[k]}\n' for k in sorted(request.headers)))
        signed_headers = ';'.join((k.lower() for k in sorted(request.headers)))
        payload_hash = sha256(request.body.encode('utf-8')).hexdigest()
        canonical_request = '\n'.join([request.method, '/', '', canonical_headers, signed_headers, payload_hash])
        algorithm = 'AWS4-HMAC-SHA256'
        credential_scope = '/'.join([timestamp[0:8], self.region, 'sts', 'aws4_request'])
        canonical_request_hash = sha256(canonical_request.encode('utf-8')).hexdigest()
        string_to_sign = '\n'.join([algorithm, timestamp, credential_scope, canonical_request_hash])
        key = f'AWS4{self.secret_key}'.encode()
        key = hmac.new(key, timestamp[0:8].encode('utf-8'), sha256).digest()
        key = hmac.new(key, self.region.encode('utf-8'), sha256).digest()
        key = hmac.new(key, b'sts', sha256).digest()
        key = hmac.new(key, b'aws4_request', sha256).digest()
        signature = hmac.new(key, string_to_sign.encode('utf-8'), sha256).hexdigest()
        authorization = '{} Credential={}/{}, SignedHeaders={}, Signature={}'.format(algorithm, self.access_key, credential_scope, signed_headers, signature)
        request.headers['Authorization'] = authorization