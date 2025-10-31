import tempfile
import os

class InitWithDirMixin:
    """A mixin to allow setting up a state dir rather than a state file. This is
    only meant to test state dir creation and permissions -- most operations are
    unlikely to work.
    """

    def _init_state(self) -> None:
        self.base_dir = tempfile.mkdtemp(prefix='inst')
        self.cfg_file = os.path.join(self.base_dir, 'config.json')
        self.cli_log_file_name = os.path.join(self.base_dir, 'cli-log')
        username = pwd.getpwuid(os.getuid())[0]
        self.user_dir = os.path.join(self.base_dir, '%s-state' % username)
        self.log_file_name = os.path.join(self.user_dir, 'log')
        self.sock_file = os.path.join(self.user_dir, 'sock')
        self.state_file = os.path.join(self.user_dir, 'state')
        self.pipe_name = 'INVALID'

    def get_state_args(self):
        return ['--test-state-dir={0}'.format(self.base_dir)]