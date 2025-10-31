import socket
import multiprocessing
import time

class AgentOpsServerManager:

    def __init__(self, daemon: bool=True, port: int | None=None):
        self.server_process: multiprocessing.Process | None = None
        self.server_port = port
        self.daemon = daemon
        logger.info('AgentOpsServerManager initialized.')

    def _find_available_port(self) -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]

    def start(self):
        if self.server_process and self.server_process.is_alive():
            logger.warning('AgentOps server process appears to be already running.')
            return
        if self.server_port is None:
            self.server_port = self._find_available_port()
        logger.info(f'Starting AgentOps local server on port {self.server_port}...')
        self.server_process = multiprocessing.Process(target=_run_server, kwargs={'host': '127.0.0.1', 'port': self.server_port, 'use_reloader': False, 'debug': False}, daemon=self.daemon, name='AgentLightning-AgentOpsServer')
        self.server_process.start()
        logger.info(f'AgentOps local server process (PID: {self.server_process.pid}) started, targeting port {self.server_port}.')
        time.sleep(0.5)
        if not self.server_process.is_alive():
            logger.error(f'AgentOps local server failed to start or exited prematurely.')

    def is_alive(self) -> bool:
        if self.server_process and self.server_process.is_alive():
            return True
        return False

    def stop(self):
        if self.is_alive():
            logger.info(f'Stopping AgentOps local server (PID: {self.server_process.pid})...')
            self.server_process.terminate()
            self.server_process.join(timeout=5)
            if self.server_process.is_alive():
                logger.warning(f'AgentOps server (PID: {self.server_process.pid}) did not terminate gracefully, killing...')
                self.server_process.kill()
                self.server_process.join(timeout=10)
            self.server_process = None
            logger.info(f'AgentOps local server stopped.')
        else:
            logger.info('AgentOps local server was not running or already stopped.')

    def get_port(self) -> int | None:
        if self.is_alive() and self.server_port is not None:
            return self.server_port
        if self.server_port is not None and (self.server_process is None or not self.server_process.is_alive()):
            logger.warning(f'AgentOps server port {self.server_port} is stored, but server process is not alive. Returning stored port.')
        return self.server_port