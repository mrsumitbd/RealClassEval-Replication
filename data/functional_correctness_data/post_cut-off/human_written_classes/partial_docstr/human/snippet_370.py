from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import threading
from omnicoreagent.core.utils import logger

class CallbackServer:
    """Simple server to handle OAuth callbacks."""

    def __init__(self, port=3000):
        self.port = port
        self.server = None
        self.thread = None
        self.callback_data = {'authorization_code': None, 'state': None, 'error': None}

    def _create_handler_with_data(self):
        """Create a handler class with access to callback data."""
        callback_data = self.callback_data

        class DataCallbackHandler(CallbackHandler):

            def __init__(self, request, client_address, server):
                super().__init__(request, client_address, server, callback_data)
        return DataCallbackHandler

    def start(self):
        """Start the callback server in a background thread."""
        handler_class = self._create_handler_with_data()
        self.server = HTTPServer(('localhost', self.port), handler_class)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        logger.info(f'🖥️  Started callback server on http://localhost:{self.port}')

    def stop(self):
        """Stop the callback server."""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
        if self.thread:
            self.thread.join(timeout=1)

    def wait_for_callback(self, timeout=300):
        """Wait for OAuth callback with timeout."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if self.callback_data['authorization_code']:
                return self.callback_data['authorization_code']
            elif self.callback_data['error']:
                raise Exception(f"OAuth error: {self.callback_data['error']}")
            time.sleep(0.1)
        raise Exception('Timeout waiting for OAuth callback')

    def get_state(self):
        """Get the received state parameter."""
        return self.callback_data['state']