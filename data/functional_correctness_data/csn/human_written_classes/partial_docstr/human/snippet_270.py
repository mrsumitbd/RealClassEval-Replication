import subprocess

class Launcher:

    def __init__(self, cmd, args=[], cwd=None):
        self.cmd = cmd
        self.args = args
        self.cwd = cwd

    def run(self):
        """Runs the cmd with args after converting them all to strings via str"""
        logger.debug(self.cwd or './')
        logger.debug('    ' + str(self))
        try:
            (subprocess.check_call(map(str, [self.cmd] + self.args), cwd=self.cwd),)
        except FileNotFoundError:
            raise RuntimeError("Command '" + self.cmd + "' not found. Make sure it is in $PATH")
        except subprocess.CalledProcessError:
            self.errormsg = '"{}" exited with an error code. See stderr for details.'
            raise RuntimeError(self.errormsg.format(str(self)))

    def __str__(self):
        return ' '.join(map(str, [self.cmd] + self.args))