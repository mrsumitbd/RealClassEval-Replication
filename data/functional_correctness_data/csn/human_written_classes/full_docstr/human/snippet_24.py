from pathlib import Path
from subprocess import CalledProcessError, CompletedProcess
from molecule.console import original_stderr
from ansible_compat.runtime import Runtime
from molecule.ansi_output import CommandBorders
from molecule.util import print_environment_vars

class App:
    """App class that keep runtime status."""

    def __init__(self, path: Path) -> None:
        """Create a new app instance.

        Args:
            path: The path to the project.
        """
        self.runtime = Runtime(project_dir=path, isolated=False)

    def run_command(self, cmd: str | list[str], env: dict[str, str] | None=None, cwd: Path | None=None, *, debug: bool=False, echo: bool=False, quiet: bool=False, check: bool=False, command_borders: bool=False) -> CompletedProcess[str]:
        """Execute the given command and returns None.

        Args:
            cmd: A list of strings containing the command to run.
            env: A dict containing the shell's environment.
            cwd: An optional Path to the working directory.
            debug: An optional bool to toggle debug output.
            echo: An optional bool to toggle command echo.
            quiet: An optional bool to toggle command output.
            check: An optional bool to toggle command error checking.
            command_borders: An optional bool to enable borders around command output.

        Returns:
            A completed process object.

        Raises:
            CalledProcessError: If return code is nonzero and check is True.
        """
        if debug:
            print_environment_vars(env)
        borders = None
        if command_borders:
            borders = CommandBorders(cmd=cmd, original_stderr=original_stderr)
        result = self.runtime.run(args=cmd, env=env, cwd=cwd, tee=True, set_acp=False)
        if borders:
            borders.finalize(result.returncode)
        if result.returncode != 0 and check:
            raise CalledProcessError(returncode=result.returncode, cmd=result.args, output=result.stdout, stderr=result.stderr)
        return result