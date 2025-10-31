import struct
import pty
import signal
import sys
import fcntl
import os
from typing import Any, Callable, Dict, List, Optional, Type
import select
import termios
import traceback
import threading

class PtyManager:
    """Manages PTY-based Python execution with state synchronization."""

    def __init__(self, callback: Optional[Callable]=None):
        self.supervisor_fd = -1
        self.worker_fd = -1
        self.pid = -1
        self.output_buffer: List[str] = []
        self.input_buffer: List[str] = []
        self.stop_event = threading.Event()
        self.callback = callback

    def start(self, code: str) -> None:
        """Start PTY session with code execution."""
        self.supervisor_fd, self.worker_fd = pty.openpty()
        term_size = struct.pack('HHHH', 24, 80, 0, 0)
        fcntl.ioctl(self.worker_fd, termios.TIOCSWINSZ, term_size)
        self.pid = os.fork()
        if self.pid == 0:
            try:
                os.close(self.supervisor_fd)
                os.dup2(self.worker_fd, 0)
                os.dup2(self.worker_fd, 1)
                os.dup2(self.worker_fd, 2)
                namespace = repl_state.get_namespace()
                exec(code, namespace)
                os._exit(0)
            except Exception:
                traceback.print_exc(file=sys.stderr)
                os._exit(1)
        else:
            os.close(self.worker_fd)
            reader = threading.Thread(target=self._read_output)
            reader.daemon = True
            reader.start()
            input_handler = threading.Thread(target=self._handle_input)
            input_handler.daemon = True
            input_handler.start()

    def _read_output(self) -> None:
        """Read and process PTY output with improved error handling and file descriptor management."""
        buffer = ''
        incomplete_bytes = b''
        while not self.stop_event.is_set():
            try:
                if self.supervisor_fd < 0:
                    logger.debug('Invalid file descriptor, stopping output reader')
                    break
                try:
                    r, _, _ = select.select([self.supervisor_fd], [], [], 0.1)
                except (OSError, ValueError) as e:
                    logger.debug(f'File descriptor error during select: {e}')
                    break
                if self.supervisor_fd in r:
                    try:
                        raw_data = os.read(self.supervisor_fd, 1024)
                    except (OSError, ValueError) as e:
                        if e.errno == 9:
                            logger.debug('PTY closed, stopping output reader')
                        else:
                            logger.warning(f'Error reading from PTY: {e}')
                        break
                    if not raw_data:
                        logger.debug('EOF reached, PTY closed')
                        break
                    full_data = incomplete_bytes + raw_data
                    try:
                        data = full_data.decode('utf-8')
                        incomplete_bytes = b''
                    except UnicodeDecodeError as e:
                        if e.start > 0:
                            data = full_data[:e.start].decode('utf-8')
                            incomplete_bytes = full_data[e.start:]
                        else:
                            incomplete_bytes = full_data
                            continue
                    if data:
                        buffer += data
                        while '\n' in buffer:
                            line, buffer = buffer.split('\n', 1)
                            cleaned = clean_ansi(line + '\n')
                            self.output_buffer.append(cleaned)
                            if self.callback:
                                try:
                                    self.callback(cleaned)
                                except Exception as callback_error:
                                    logger.warning(f'Error in output callback: {callback_error}')
                        if buffer:
                            cleaned = clean_ansi(buffer)
                            if self.callback:
                                try:
                                    self.callback(cleaned)
                                except Exception as callback_error:
                                    logger.warning(f'Error in output callback: {callback_error}')
            except (OSError, IOError) as e:
                if hasattr(e, 'errno') and e.errno == 9:
                    logger.debug('PTY file descriptor closed, stopping reader')
                    break
                else:
                    logger.warning(f'I/O error reading PTY output: {e}')
                    continue
            except UnicodeDecodeError as e:
                logger.warning(f'Unicode decode error: {e}')
                incomplete_bytes = b''
                continue
            except Exception as e:
                logger.error(f'Unexpected error in _read_output: {e}')
                break
        if buffer:
            try:
                cleaned = clean_ansi(buffer)
                self.output_buffer.append(cleaned)
                if self.callback:
                    self.callback(cleaned)
            except Exception as e:
                logger.warning(f'Error processing final buffer: {e}')
        if incomplete_bytes:
            try:
                final_data = incomplete_bytes.decode('utf-8', errors='replace')
                if final_data:
                    cleaned = clean_ansi(final_data)
                    self.output_buffer.append(cleaned)
                    if self.callback:
                        self.callback(cleaned)
            except Exception as e:
                logger.warning(f'Failed to process remaining bytes at shutdown: {e}')
        logger.debug('PTY output reader thread finished')

    def _handle_input(self) -> None:
        """Handle interactive user input with improved buffering."""
        while not self.stop_event.is_set():
            try:
                r, _, _ = select.select([sys.stdin], [], [], 0.1)
                if sys.stdin in r:
                    input_data = ''
                    while True:
                        char = sys.stdin.read(1)
                        if not char or char == '\n':
                            input_data += '\n'
                            break
                        input_data += char
                    if input_data:
                        if input_data not in self.input_buffer:
                            self.input_buffer.append(input_data)
                            os.write(self.supervisor_fd, input_data.encode())
            except (OSError, IOError):
                break

    def get_output(self) -> str:
        """Get complete output with ANSI codes removed and binary content truncated."""
        raw = ''.join(self.output_buffer)
        clean = clean_ansi(raw)

        def format_binary(text: str, max_len: int=None) -> str:
            if max_len is None:
                max_len = int(os.environ.get('PYTHON_REPL_BINARY_MAX_LEN', '100'))
            if '\\x' in text and len(text) > max_len:
                return f'{text[:max_len]}... [binary content truncated]'
            return text
        return format_binary(clean)

    def stop(self) -> None:
        """Stop PTY session and clean up resources properly."""
        logger.debug('Stopping PTY session...')
        self.stop_event.set()
        if self.pid > 0:
            try:
                os.kill(self.pid, signal.SIGTERM)
                try:
                    pid, status = os.waitpid(self.pid, os.WNOHANG)
                    if pid == 0:
                        import time
                        time.sleep(0.1)
                        pid, status = os.waitpid(self.pid, os.WNOHANG)
                        if pid == 0:
                            logger.debug('Forcing process termination')
                            os.kill(self.pid, signal.SIGKILL)
                            os.waitpid(self.pid, 0)
                except OSError as e:
                    logger.debug(f'Process cleanup error (likely already exited): {e}')
            except (OSError, ProcessLookupError) as e:
                logger.debug(f'Process termination error (likely already gone): {e}')
            finally:
                self.pid = -1
        if self.supervisor_fd >= 0:
            try:
                os.close(self.supervisor_fd)
                logger.debug('PTY supervisor file descriptor closed')
            except OSError as e:
                logger.debug(f'Error closing supervisor fd: {e}')
            finally:
                self.supervisor_fd = -1
        logger.debug('PTY session cleanup completed')