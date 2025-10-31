
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

    def __init__(self, name, port=0, aliases=None, broadcast_interval=2,
                 nameservers=None, min_port=None, max_port=None):
        # Build configuration dictionary for the publisher
        self._config = {
            'name': name,
            'port': port,
            'aliases': aliases,
            'broadcast_interval': broadcast_interval,
            'nameservers': nameservers,
            'min_port': min_port,
            'max_port': max_port
        }
        self.publisher = None

    def __enter__(self):
        # Create the publisher instance from the configuration
        self.publisher = create_publisher_from_dict_config(self._config)
        # Start the publisher thread
        self.publisher.start()
        return self.publisher

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Stop the publisher if it was started
        if self.publisher:
            try:
                self.publisher.stop()
            except Exception:
                pass
            try:
                self.publisher.join()
            except Exception:
                pass
        # Propagate any exception that occurred
        return False
