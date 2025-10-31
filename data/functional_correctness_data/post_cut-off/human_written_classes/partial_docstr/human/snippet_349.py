import weakref
import os
import threading
import time
import signal
from gettext import gettext as _

class SSHProcessManager:
    """Manages SSH processes and ensures proper cleanup"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.processes = {}
            cls._instance.terminals = weakref.WeakSet()
            cls._instance.lock = threading.Lock()
            cls._instance.cleanup_thread = None
            cls._instance._start_cleanup_thread()
        return cls._instance

    def _start_cleanup_thread(self):
        """Start background cleanup thread"""
        logger.debug('Automatic SSH cleanup thread disabled to prevent race conditions')

    def _cleanup_loop(self):
        """Background cleanup loop"""
        while True:
            try:
                time.sleep(60)
                self._cleanup_orphaned_processes()
            except Exception as e:
                logger.error(f'Error in cleanup loop: {e}')

    def _cleanup_orphaned_processes(self):
        """Clean up processes not tracked by active terminals"""
        with self.lock:
            active_pids = set()
            for terminal in list(self.terminals):
                try:
                    pid = getattr(terminal, 'process_pid', None)
                    if pid:
                        active_pids.add(pid)
                        logger.debug(f'Terminal {id(terminal)} has active PID {pid}')
                except Exception as e:
                    logger.debug(f'Error getting stored PID from terminal: {e}')
            import time
            current_time = time.time()
            orphaned_pids = []
            for pid in list(self.processes.keys()):
                if pid not in active_pids:
                    process_info = self.processes.get(pid, {})
                    start_time = process_info.get('start_time')
                    if start_time and hasattr(start_time, 'timestamp'):
                        process_age = current_time - start_time.timestamp()
                        if process_age < 600:
                            logger.debug(f'Process {pid} is only {process_age:.1f}s old, skipping cleanup')
                            continue
                    else:
                        logger.debug(f'Process {pid} has no start_time info, skipping cleanup')
                        continue
                    try:
                        os.kill(pid, 0)
                        orphaned_pids.append(pid)
                        logger.debug(f'Found orphaned process {pid} (age: {process_age:.1f}s)')
                    except ProcessLookupError:
                        logger.debug(f'Process {pid} already gone, removing from tracking')
                        if pid in self.processes:
                            del self.processes[pid]
                    except Exception as e:
                        logger.debug(f'Error checking process {pid}: {e}')
            for pid in orphaned_pids:
                logger.info(f'Cleaning up orphaned process {pid}')
                self._terminate_process_by_pid(pid)

    def _terminate_process_by_pid(self, pid):
        """Terminate a process by PID"""
        try:
            pgid = os.getpgid(pid)
            os.killpg(pgid, signal.SIGTERM)
            for _ in range(10):
                try:
                    os.killpg(pgid, 0)
                    time.sleep(0.1)
                except ProcessLookupError:
                    return True
            os.killpg(pgid, signal.SIGKILL)
            return True
        except Exception:
            return False

    def register_terminal(self, terminal):
        """Register a terminal for tracking"""
        self.terminals.add(terminal)
        logger.debug(f'Registered terminal {id(terminal)}')

    def cleanup_all(self):
        """Clean up all managed processes"""
        import signal

        def timeout_handler(signum, frame):
            logger.warning('Cleanup timeout - forcing exit')
            os._exit(1)
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(5)
        try:
            logger.info('Cleaning up all SSH processes...')
            for terminal in list(self.terminals):
                terminal._is_quitting = True
            with self.lock:
                processes_to_clean = dict(self.processes)
                self.processes.clear()
            for pid, info in processes_to_clean.items():
                logger.debug(f"Cleaning up process {pid} (command: {info.get('command', 'unknown')})")
                self._terminate_process_by_pid(pid)
            for terminal in list(self.terminals):
                try:
                    if hasattr(terminal, 'disconnect') and hasattr(terminal, 'is_connected') and terminal.is_connected:
                        logger.debug(f'Disconnecting terminal {id(terminal)}')
                        terminal.disconnect()
                except Exception as e:
                    logger.error(f'Error cleaning up terminal {id(terminal)}: {e}')
            self.terminals.clear()
            logger.info('SSH process cleanup completed')
        finally:
            signal.alarm(0)