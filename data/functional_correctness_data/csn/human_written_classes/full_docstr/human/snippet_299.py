from posttroll.address_receiver import get_configured_address_port

class _AddressListener:
    """Listener for new addresses of interest."""

    def __init__(self, subscriber, services='', nameserver='localhost'):
        """Initialize address listener."""
        if isinstance(services, str):
            services = [services]
        self.services = services
        self.subscriber = subscriber
        address_publish_port = get_configured_address_port()
        self.subscriber.add_hook_sub('tcp://' + nameserver + ':' + str(address_publish_port), ['pytroll://address'], self.handle_msg)

    def handle_msg(self, msg):
        """Handle the message *msg*."""
        addr_ = msg.data['URI']
        status = msg.data.get('status', True)
        if status:
            msg_services = msg.data.get('service')
            for service in self.services:
                if not service or service in msg_services:
                    LOGGER.debug('Adding address %s %s', str(addr_), str(service))
                    self.subscriber.add(addr_)
                    break
        else:
            LOGGER.debug('Removing address %s', str(addr_))
            self.subscriber.remove(addr_)