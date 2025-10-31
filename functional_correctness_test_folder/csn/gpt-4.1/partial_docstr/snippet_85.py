
class SessionListener:
    '''Base class for :class:`Session` listeners, which are notified when a new
    NETCONF message is received or an error occurs.
    .. note::
        Avoid time-intensive tasks in a callback's context.
    '''

    def callback(self, root, raw):
        """
        Called when a new NETCONF message is received.

        :param root: The parsed XML root element of the message.
        :param raw: The raw message string.
        """
        pass

    def errback(self, ex):
        '''Called when an error occurs.
        :type ex: :exc:`Exception`
        '''
        pass
