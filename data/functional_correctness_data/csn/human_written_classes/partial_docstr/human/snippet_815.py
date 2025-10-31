from wampy.errors import WampyError, WampProtocolError
from wampy.messages.call import Call
from wampy.constants import NOT_AUTHORISED
from wampy.messages import Error, Result
from wampy.messages import MESSAGE_TYPE_MAP

class RpcProxy:
    """ Proxy wrapper of a `wampy` client for WAMP application RPCs
    where the endpoint is a non-delimted single string name, such as
    a function name, e.g. ::

        "get_data"

    The typical use case of this proxy class is for microservices
    where endpoints are class methods.

    """

    def __init__(self, client):
        self.client = client

    def __getattr__(self, name):

        def wrapper(*args, **kwargs):
            options = {'timeout': int(self.client.call_timeout * 1000)}
            message = Call(procedure=name, options=options, args=args, kwargs=kwargs)
            response = self.client._make_rpc(message)
            wamp_code = response.WAMP_CODE
            if wamp_code == Error.WAMP_CODE:
                _, _, request_id, _, endpoint, exc_args, exc_kwargs = response.message
                if endpoint == NOT_AUTHORISED:
                    raise WampyError('NOT_AUTHORISED: {} - {}'.format(self.client.name, exc_args[0]))
                raise WampyError('oops! wampy has failed, sorry: {}'.format(response.message))
            if wamp_code != Result.WAMP_CODE:
                raise WampProtocolError('unexpected message code: "%s (%s) %s"', wamp_code, MESSAGE_TYPE_MAP[wamp_code], response[5])
            result = response.value
            logger.debug('RpcProxy got result: %s', result)
            return result
        return wrapper