import logging
import os
import shlex
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Mapping, Optional, Sequence, Union


def _ensure_text(s: Union[str, Path, None]) -> Optional[str]:
    if s is None:
        return None
    return str(s)


def _system_encoding() -> str:
    import locale

    return locale.getpreferredencoding(False) or "utf-8"


@dataclass
class _Result:
    returncode: int
    stdout: Optional[Union[str, bytes]]
    stderr: Optional[Union[str, bytes]]


@dataclass
class Command:
    run: str
    save: bool = False
    cwd: Optional[Path] = None
    as_bytes: bool = False
    encoding: Optional[str] = None
    stdout_path: Optional[str] = None
    stderr_path: Optional[str] = None
    append: bool = False

    def _open_target(self, path: Optional[str], mode_write: str):
        if not path:
            return None
        if path == "/dev/null":
            return open(os.devnull, mode_write)
        # Only applicable to stderr
        if path == "/dev/stdout":
            return subprocess.STDOUT
        return open(path, mode_write)

    def _prepare_args(self, shell: bool) -> Union[str, Sequence[str]]:
        if shell:
            return self.run
        return shlex.split(self.run)

    def execute(self, shell: bool) -> _Result:
        closeables: List[Any] = []
        try:
            mode = "ab" if self.append else "wb"
            stdout_target = None
            stderr_target = None

            if self.stdout_path:
                stdout_target = self._open_target(self.stdout_path, mode)
                if hasattr(stdout_target, "close"):
                    closeables.append(stdout_target)

            if self.stderr_path:
                stderr_target = self._open_target(self.stderr_path, mode)
                # _open_target could return subprocess.STDOUT sentinel; don't close that.
                if hasattr(stderr_target, "close"):
                    closeables.append(stderr_target)

            capture_needed = self.save and not (stdout_target or stderr_target)
            run_kwargs = {
                "shell": shell,
                "cwd": str(self.cwd) if self.cwd else None,
                "stdout": subprocess.PIPE if capture_needed else stdout_target,
                "stderr": subprocess.PIPE if capture_needed else stderr_target,
                "text": False,  # always get bytes, we handle decoding ourselves
            }

            completed = subprocess.run(self._prepare_args(
                shell), **run_kwargs)  # type: ignore[arg-type]

            out_bytes = None
            err_bytes = None

            if capture_needed:
                out_bytes = completed.stdout
                err_bytes = completed.stderr

            if self.save:
                if self.as_bytes:
                    out_val = out_bytes if out_bytes not in (
                        b"", None) else None
                    err_val = err_bytes if err_bytes not in (
                        b"", None) else None
                else:
                    enc = self.encoding or _system_encoding()
                    out_val = (
                        out_bytes.decode(enc, errors="replace").rstrip("\r\n")
                        if out_bytes not in (b"", None)
                        else None
                    )
                    err_val = (
                        err_bytes.decode(enc, errors="replace").rstrip("\r\n")
                        if err_bytes not in (b"", None)
                        else None
                    )
            else:
                out_val = None
                err_val = None

            return _Result(
                returncode=completed.returncode,
                stdout=out_val,
                stderr=err_val,
            )
        finally:
            for c in closeables:
                try:
                    c.close()
                except Exception:
                    pass


class CmdStep:
    '''A pypyr step to run an executable or command as a subprocess.
    This models a step that takes config like this:
        cmd: <<cmd string>>
    OR, expanded syntax is as a dict
        cmd:
            run: str. mandatory. command + args to execute.
            save: bool. defaults False. save output to cmdOut. Treats output
                as text in the system's encoding and removes newlines at end.
            cwd: str/Pathlike. optional. Working directory for this command.
            bytes (bool): Default False. When `save` return output bytes from
                cmd unaltered, without applying any encoding & text newline
                processing.
            encoding (str): Default None. When `save`, decode cmd output with
                this encoding. The default of None uses the system encoding and
                should "just work".
            stdout (str | Path): Default None. Write stdout to this file path.
                Special value `/dev/null` writes to the system null device.
            stderr (str | Path): Default None. Write stderr to this file path.
                Special value `/dev/null` writes to the system null device.
                Special value `/dev/stdout` redirects err output to stdout.
            append (bool): Default False. When stdout/stderr a file, append
                rather than overwrite. Default is to overwrite.
    In expanded syntax, `run` can be a simple string or a list:
        cmd:
          run:
            - my-executable --arg
            - cmd here
          save: False
          cwd: ./path/here
    OR, as a list in simplified syntax:
        cmd:
          - my-executable --arg
          - ./another-executable --arg
    Any or all of the list items can use expanded syntax:
        cmd:
          - ./simple-cmd-here --arg1 value
          - run: cmd here
            save: False
            cwd: ./path/here
          - run:
              - my-executable --arg
              - ./another-executable --arg
            save: True cwd: ./path/here
    If save is True, will save the output to context as follows:
        cmdOut:
            returncode: 0
            stdout: 'stdout str here. None if empty.'
            stderr: 'stderr str here. None if empty.'
    If the cmd input contains a list of executables, cmdOut will be a list of
    cmdOut objects, in order executed.
    cmdOut.returncode is the exit status of the called process. Typically 0
    means OK. A negative value -N indicates that the child was terminated by
    signal N (POSIX only).
    The run_step method does the actual work. init parses the input yaml.
    Attributes:
        logger (logger): Logger instantiated by name of calling step.
        context: (pypyr.context.Context): The current pypyr Context.
        commands (list[pypyr.subproc.Command]): Commands to run as subprocess.
        is_shell (bool): True if subprocess should run through default shell.
        name (str): Name of calling step. Used for logging output & error
            messages.
    '''

    def __init__(self, name: str, context: Mapping[str, Any], is_shell: bool = False) -> None:
        '''Initialize the CmdStep.
        The step config in the context dict in simplified syntax:
            cmd: <<cmd string>>
        OR, as a dict in expanded syntax:
            cmd:
                run: str. mandatory. command + args to execute.
                save: bool. optional. defaults False. save output to cmdOut.
                cwd: str/path. optional. if specified, change the working
                     directory just for the duration of the command.
        `run` can be a single string, or it can be a list of string if there
        are multiple commands to execute with the same settings.
        OR, as a list:
            cmd:
                - my-executable --arg
                - ./another-executable --arg
        Any or all of the list items can be in expanded syntax.
        Args:
            name (str): Unique name for step. Likely __name__ of calling step.
            context (pypyr.context.Context): Look for step config in this
                context instance.
            is_shell (bool): Set to true to execute cmd through the default
                shell.
        '''
        self.name = name
        self.logger = logging.getLogger(name)
        self.context = context  # treat as Mapping; writer later uses __setitem__ if dict-like
        self.is_shell = is_shell
        self.commands: List[Command] = []

        if "cmd" not in context:
            raise KeyError("Missing required 'cmd' in context.")

        raw = context["cmd"]

        def add_command_from_expanded(expanded: Mapping[str, Any]) -> None:
            run_val = expanded.get("run")
            if run_val is None:
                raise ValueError("Expanded cmd dict must contain 'run'.")
            runs: Iterable[str]
            if isinstance(run_val, str):
                runs = [run_val]
            elif isinstance(run_val, list) or isinstance(run_val, tuple):
                if not all(isinstance(x, str) for x in run_val):
                    raise TypeError("All items in 'run' list must be strings.")
                runs = run_val  # type: ignore[assignment]
            else:
                raise TypeError("'run' must be a string or a list of strings.")

            for r in runs:
                cmd = self.create_command(
                    {
                        "run": r,
                        "save": expanded.get("save", False),
                        "cwd": expanded.get("cwd"),
                        "bytes": expanded.get("bytes", False),
                        "encoding": expanded.get("encoding"),
                        "stdout": expanded.get("stdout"),
                        "stderr": expanded.get("stderr"),
                        "append": expanded.get("append", False),
                    }
                )
                self.commands.append(cmd)

        if isinstance(raw, str):
            self.commands.append(self.create_command({"run": raw}))
        elif isinstance(raw, Mapping):
            add_command_from_expanded(raw)
        elif isinstance(raw, list) or isinstance(raw, tuple):
            for item in raw:
                if isinstance(item, str):
                    self.commands.append(self.create_command({"run": item}))
                elif isinstance(item, Mapping):
                    add_command_from_expanded(item)
                else:
                    raise TypeError(
                        "Items in cmd list must be str or mapping.")
        else:
            raise TypeError("cmd must be a str, mapping or list.")

    def create_command(self, cmd_input: Mapping) -> Command:
        '''Create a pypyr.subproc.Command object from expanded step input.'''
        run = cmd_input.get("run")
        if not isinstance(run, str):
            raise TypeError("'run' must be a string.")
        save = bool(cmd_input.get("save", False))
        cwd = cmd_input.get("cwd")
        cwd_path = Path(cwd).resolve() if cwd is not None else None
        as_bytes = bool(cmd_input.get("bytes", False))
        encoding = cmd_input.get("encoding")
        if encoding is not None and not isinstance(encoding, str):
            raise TypeError("'encoding' must be a string when provided.")
        stdout_path = _ensure_text(cmd_input.get("stdout"))
        stderr_path = _ensure_text(cmd_input.get("stderr"))
        append = bool(cmd_input.get("append", False))

        return Command(
            run=run,
            save=save,
            cwd=cwd_path,
            as_bytes=as_bytes,
            encoding=encoding,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            append=append,
        )

    def run_step(self) -> None:
        '''Spawn a subprocess to run the command or program.
        If cmd.is_save==True, save result of each command to context 'cmdOut'.
        '''
        results: List[dict] = []
        any_saved = False

        for cmd in self.commands:
            self.logger.debug("Executing command: %s", cmd.run)
            res = cmd.execute(shell=self.is_shell)
            if cmd.save:
                any_saved = True
                results.append(
                    {
                        "returncode": res.returncode,
                        "stdout": res.stdout,
                        "stderr": res.stderr,
                    }
                )

        if any_saved:
            out_obj: Union[dict, List[dict]]
            if len(results) == 1:
                out_obj = results[0]
            else:
                out_obj = results

            # Attempt to set into context if it's mutable like a dict.
            try:
                self.context["cmdOut"] = out_obj  # type: ignore[index]
            except Exception:
                pass

        self.logger.debug("Command(s) completed.")
