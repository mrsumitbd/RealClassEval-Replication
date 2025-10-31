class QRebootProtocol:
    """ Oqus/Miqus/Arqus discovery protocol implementation"""

    def __init__(self):
        self.transport = None

    def connection_made(self, transport):
        """ On socket creation """
        self.transport = transport

    def send_reboot(self):
        """ Sends reboot package broadcast """
        self.transport.sendto(b'reboot', ('<broadcast>', DEFAULT_DISCOVERY_PORT))