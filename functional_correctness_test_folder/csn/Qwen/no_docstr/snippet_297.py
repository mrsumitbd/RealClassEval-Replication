
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
        from posttroll.publisher import get_publisher
        self.publisher = get_publisher(
            name, port, aliases, broadcast_interval, nameservers, min_port, max_port)

    def __enter__(self):
        self.publisher.start()
        return self.publisher

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.publisher.stop()
