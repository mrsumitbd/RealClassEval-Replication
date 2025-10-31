
class SessionListener:
    '''Base class for :class:`Session` listeners, which are notified when a new
    NETCONF message is received or an error occurs.
    .. note::
        Avoid time-intensive tasks in a callback's context.
    '''

    def callback(self, root, raw):
        '''Called when a new NETCONF message is received.
        :param root: The root element of the received message.
        :type root: :class:`xml.etree.ElementTree.Element`
        :param raw: The raw XML string of the received message.
        :type raw: str
        '''
        pass

    def errback(self, ex):
        '''Called when an error occurs.
        :type ex: :exc:`Exception`
        '''
        pass
