import ssl
from aredis.exceptions import ConnectionError, TimeoutError, RedisError, ExecAbortError, BusyLoadingError, NoScriptError, ReadOnlyError, ResponseError, InvalidResponse, AskError, MovedError, TryAgainError, ClusterDownError, ClusterCrossSlotError

class RedisSSLContext:

    def __init__(self, keyfile=None, certfile=None, cert_reqs=None, ca_certs=None):
        self.keyfile = keyfile
        self.certfile = certfile
        if cert_reqs is None:
            self.cert_reqs = ssl.CERT_NONE
        elif isinstance(cert_reqs, str):
            CERT_REQS = {'none': ssl.CERT_NONE, 'optional': ssl.CERT_OPTIONAL, 'required': ssl.CERT_REQUIRED}
            if cert_reqs not in CERT_REQS:
                raise RedisError('Invalid SSL Certificate Requirements Flag: %s' % cert_reqs)
            self.cert_reqs = CERT_REQS[cert_reqs]
        self.ca_certs = ca_certs
        self.context = None

    def get(self):
        if not self.keyfile:
            self.context = ssl.create_default_context(cafile=self.ca_certs)
        else:
            self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
            self.context.verify_mode = self.cert_reqs
            self.context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)
            self.context.load_verify_locations(self.ca_certs)
        return self.context