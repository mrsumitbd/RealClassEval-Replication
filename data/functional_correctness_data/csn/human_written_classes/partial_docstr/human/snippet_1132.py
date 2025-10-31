import shlex
import termcolor

class Git:
    """
    A stateful helper class for formatting git commands.

    To avoid confusion, and because these are not directly relevant to users,
    the class variables ``cache`` and ``working_area`` are excluded from logs.

    Example usage::

        command = Git().set("-C {folder}", folder="foo")("git clone {repo}", repo="foo")
        print(command)
    """
    cache = ''
    working_area = ''

    def __init__(self):
        self._args = []

    def set(self, git_arg, **format_args):
        """git = Git().set("-C {folder}", folder="foo")"""
        format_args = {name: shlex.quote(arg) for name, arg in format_args.items()}
        git = Git()
        git._args = self._args[:]
        git._args.append(git_arg.format(**format_args))
        return git

    def __call__(self, command, **format_args):
        """Git()("git clone {repo}", repo="foo")"""
        git = self.set(command, **format_args)
        git_command = f"git {' '.join(git._args)}"
        logged_command = f"git {' '.join((arg for arg in git._args if arg not in [str(git.cache), str(Git.working_area)]))}"
        logger.info(termcolor.colored(logged_command, attrs=['bold']))
        return git_command