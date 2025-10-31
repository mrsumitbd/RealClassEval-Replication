
class SessionListener:
    '''Base class for :class:`Session` listeners, which are notified when a new
    NETCONF message is received or an error occurs.
    .. note::
        Avoid time-intensive tasks in a callback's context.
    '''

    def callback(self, root, raw):
        '''Called when a new NETCONF message is received.

        :param root: XML root element of the message.
        :param raw: Raw XML string of the message.
        '''
        raise NotImplementedError("Subclasses must implement 'callback'")

    def errback(self, ex):
        '''Called when an error occurs.

        :type ex: :exc:`Exception`
        '''
        raise NotImplementedError("Subclasses must implement 'errback'")
