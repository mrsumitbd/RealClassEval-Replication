import os
import uuid
import tempfile

class InitWithFilesMixin:

    def _init_state(self) -> None:
        self.base_dir = tempfile.mkdtemp(prefix='inst')
        self.user_dir = None
        self.cfg_file = os.path.join(self.base_dir, 'config.json')
        self.log_file_name = os.path.join(self.base_dir, 'log')
        self.cli_log_file_name = os.path.join(self.base_dir, 'cli-log')
        self.pid_file = os.path.join(self.base_dir, 'pid')
        self.pipe_name = '\\\\.\\pipe\\watchman-test-%s' % uuid.uuid5(uuid.NAMESPACE_URL, self.base_dir).hex
        self.sock_file = os.path.join(self.base_dir, 'sock')
        self.state_file = os.path.join(self.base_dir, 'state')

    def get_state_args(self):
        return ['--unix-listener-path={0}'.format(self.sock_file), '--named-pipe-path={0}'.format(self.pipe_name), '--logfile={0}'.format(self.log_file_name), '--statefile={0}'.format(self.state_file), '--pidfile={0}'.format(self.pid_file)]