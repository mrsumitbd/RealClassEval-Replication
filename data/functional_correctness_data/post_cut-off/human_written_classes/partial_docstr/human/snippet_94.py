import atexit
import logging
import threading

class Server:

    def __init__(self, httpd, server_thread):
        self.httpd = httpd
        self.server_thread = server_thread
        self.logs = []
        self._stopped = False
        self.log_handler = ListHandler(self.logs)
        self.log_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(self.log_handler)
        logger.setLevel(logging.INFO)
        atexit.register(self.stop)

    def stop(self):
        if self._stopped:
            return
        self._stopped = True
        logger.info('Stopping server...')
        try:
            self.httpd.socket.close()
        except Exception as e:
            logger.debug(f'Error closing socket: {e}')
        shutdown_thread = threading.Thread(target=self.httpd.shutdown)
        shutdown_thread.daemon = True
        shutdown_thread.start()
        shutdown_thread.join(timeout=5)
        self.server_thread.join(timeout=5)
        try:
            self.httpd.server_close()
        except Exception as e:
            logger.debug(f'Error during server_close: {e}')
        logger.info('Server stopped')
        logger.removeHandler(self.log_handler)
        atexit.unregister(self.stop)

    def get_logs(self):
        """Return the current log messages."""
        return self.logs