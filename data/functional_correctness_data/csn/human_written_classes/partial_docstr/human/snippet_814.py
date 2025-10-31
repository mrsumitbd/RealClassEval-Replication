from wampy.messages.call import Call
from wampy.messages import Error, Result
from wampy.errors import WampyError, WampProtocolError

class CallProxy:
    """ Proxy wrapper of a `wampy` client for WAMP application RPCs.

    Applictions and their endpoints are identified by dot delimented
    strings, e.g. ::

        "com.example.endpoints"

    and a `CallProxy` object will call such and endpoint, passing in
    any `args` or `kwargs` necessary.

    """

    def __init__(self, client):
        self.client = client

    def __call__(self, procedure, *args, **kwargs):
        message = Call(procedure=procedure, args=args, kwargs=kwargs)
        response = self.client._make_rpc(message)
        wamp_code = response.WAMP_CODE
        if wamp_code == Error.WAMP_CODE:
            logger.error('call returned an error: %s', response)
            return response
        elif wamp_code == Result.WAMP_CODE:
            return response.value
        raise WampProtocolError('unexpected response: %s', response)