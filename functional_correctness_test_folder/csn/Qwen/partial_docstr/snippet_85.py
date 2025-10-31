
class SessionListener:
    '''Base class for :class:`Session` listeners, which are notified when a new
    NETCONF message is received or an error occurs.
    .. note::
        Avoid time-intensive tasks in a callback's context.
    '''

    def callback(self, root, raw):
        pass

    def errback(self, ex):
        '''Called when an error occurs.
        :type ex: :exc:`Exception`
        '''
        pass
