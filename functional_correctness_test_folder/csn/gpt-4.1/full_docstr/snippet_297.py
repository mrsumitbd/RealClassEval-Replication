
from posttroll.publisher import create_publisher_from_dict_config


class Publish:
    '''The publishing context.
    See :class:`Publisher` and :class:`NoisyPublisher` for more information on the arguments.
    The publisher is selected based on the arguments, see :func:`create_publisher_from_dict_config` for
    information how the selection is done.
    Example on how to use the :class:`Publish` context::
            from posttroll.publisher import Publish
            from posttroll.message import Message
            import time
            try:
                with Publish("my_service", port=9000) as pub:
                    counter = 0
                    while True:
                        counter += 1
                        message = Message("/counter", "info", str(counter))
                        print("publishing", message)
                        pub.send(message.encode())
                        time.sleep(3)
            except KeyboardInterrupt:
                print("terminating publisher...")
    '''

    def __init__(self, name, port=0, aliases=None, broadcast_interval=2, nameservers=None, min_port=None, max_port=None):
        '''Initialize the class.'''
        self._config = {
            "name": name,
            "port": port,
            "aliases": aliases,
            "broadcast_interval": broadcast_interval,
            "nameservers": nameservers,
            "min_port": min_port,
            "max_port": max_port
        }
        # Remove None values to avoid passing them to the publisher
        self._config = {k: v for k, v in self._config.items() if v is not None}
        self._publisher = None

    def __enter__(self):
        '''Enter the context.'''
        self._publisher = create_publisher_from_dict_config(self._config)
        return self._publisher

    def __exit__(self, exc_type, exc_val, exc_tb):
        '''Exit the context.'''
        if self._publisher is not None:
            self._publisher.close()
            self._publisher = None
