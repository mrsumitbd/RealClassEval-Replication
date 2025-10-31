import zmq
import threading
import time
import sys

class DotProgressBar:

    def __init__(self, context, interval=1):
        self.context = context
        self.interval = interval * 1000
        self._subprogressbar_size = 25
        self._substep_last_updated = time.time()
        self.stop_event = threading.Event()
        self._substep_cnt = 0
        self.progress_push_socket = create_socket(self.context, zmq.PUSH, 'progress push')
        self.progress_port = self.progress_push_socket.bind_to_random_port('tcp://127.0.0.1')
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        progress_pull_socket = create_socket(self.context, zmq.PULL, 'progress pull')
        progress_pull_socket.connect(f'tcp://127.0.0.1:{self.progress_port}')
        sys.stderr.write('\x1b[32m[\x1b[0m')
        sys.stderr.flush()
        _pulse_cnt = 0
        while True:
            if self.stop_event.is_set():
                return
            if not progress_pull_socket.poll(self.interval):
                if _pulse_cnt == 10:
                    sys.stderr.write('\x08 \x08' * _pulse_cnt)
                    _pulse_cnt = 0
                else:
                    sys.stderr.write('\x1b[97m.\x1b[0m')
                    _pulse_cnt += 1
                sys.stderr.flush()
            else:
                msg = progress_pull_socket.recv().decode()
                sys.stderr.write('\x08 \x08' * _pulse_cnt + msg)
                _pulse_cnt = 0
                sys.stderr.flush()

    def update(self, prog_type, status=None):
        if prog_type == 'substep_ignored':
            if time.time() - self._substep_last_updated < 1:
                return
            if self._substep_cnt == self._subprogressbar_size:
                update_str = '\x08 \x08' * self._substep_cnt + '\x1b[90m.\x1b[0m'
                self._substep_cnt = 0
            else:
                update_str = '\x1b[90m.\x1b[0m'
            self._substep_cnt += 1
            self._substep_last_updated = time.time()
        elif prog_type == 'substep_completed':
            if time.time() - self._substep_last_updated < 1:
                return
            if self._substep_cnt == self._subprogressbar_size:
                update_str = '\x08 \x08' * self._substep_cnt + '\x1b[32m.\x1b[0m'
                self._substep_cnt = 0
            else:
                update_str = '\x1b[32m.\x1b[0m'
            self._substep_cnt += 1
            self._substep_last_updated = time.time()
        elif prog_type == 'step_completed':
            update_str = '\x08 \x08' * self._substep_cnt
            self._substep_cnt = 0
            if status == 1:
                update_str += '\x1b[32m#\x1b[0m'
            elif status == 0:
                update_str += '\x1b[90m#\x1b[0m'
            elif status > 0:
                update_str += '\x1b[36m#\x1b[0m'
            else:
                update_str += '\x1b[33m#\x1b[0m'
        elif prog_type == 'done':
            update_str = '\x08 \x08' * self._substep_cnt + f'\x1b[32m]\x1b[0m {status}\n'
            self._substep_cnt = 0
        self.progress_push_socket.send(update_str.encode())

    def done(self, msg):
        self.update('done', msg)
        self.stop_event.set()