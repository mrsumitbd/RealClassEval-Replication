from typing import Any, Dict, List, Literal, Tuple, Union
import select
import tty
import pty
import os
import signal
import sys
import queue
import termios
import time

class CommandExecutor:
    """Handles execution of shell commands with timeout."""

    def __init__(self, timeout: int=None) -> None:
        self.timeout = int(os.environ.get('SHELL_DEFAULT_TIMEOUT', '900')) if timeout is None else timeout
        self.output_queue: queue.Queue = queue.Queue()
        self.exit_code = None
        self.error = None

    def execute_with_pty(self, command: str, cwd: str, non_interactive_mode: bool) -> Tuple[int, str, str]:
        """Execute command with PTY and timeout support."""
        output = []
        start_time = time.time()
        old_tty = None
        pid = -1
        if not non_interactive_mode:
            try:
                old_tty = termios.tcgetattr(sys.stdin)
            except BaseException:
                non_interactive_mode = True
        try:
            pid, fd = pty.fork()
            if pid == 0:
                try:
                    os.chdir(cwd)
                    os.execvp('/bin/sh', ['/bin/sh', '-c', command])
                except Exception as e:
                    logger.debug(f'Error in child: {e}')
                    sys.exit(1)
            else:
                if not non_interactive_mode and old_tty:
                    tty.setraw(sys.stdin.fileno())
                while True:
                    if time.time() - start_time > self.timeout:
                        try:
                            os.killpg(os.getpgid(pid), signal.SIGTERM)
                        except ProcessLookupError:
                            pass
                        raise TimeoutError(f'Command timed out after {self.timeout} seconds')
                    fds_to_watch = [fd]
                    if not non_interactive_mode:
                        fds_to_watch.append(sys.stdin)
                    try:
                        readable, _, _ = select.select(fds_to_watch, [], [], 0.1)
                    except (select.error, ValueError):
                        logger.debug('select() failed, assuming process ended.')
                        break
                    if fd in readable:
                        try:
                            data = read_output(fd)
                            if not data:
                                break
                            output.append(data)
                            sys.stdout.write(data)
                            sys.stdout.flush()
                        except OSError:
                            break
                    if not non_interactive_mode and sys.stdin in readable:
                        try:
                            stdin_data = os.read(sys.stdin.fileno(), 1024)
                            os.write(fd, stdin_data)
                        except OSError:
                            break
                try:
                    _, status = os.waitpid(pid, 0)
                    if os.WIFEXITED(status):
                        exit_code = os.WEXITSTATUS(status)
                    else:
                        exit_code = -1
                except OSError:
                    exit_code = -1
                return (exit_code, ''.join(output), '')
        finally:
            if not non_interactive_mode and old_tty:
                termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, old_tty)