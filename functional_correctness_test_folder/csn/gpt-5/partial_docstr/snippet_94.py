from __future__ import annotations

import logging
import os
import shlex
import subprocess
from pathlib import Path
from typing import Any, Mapping, Optional, Union, List


try:
    from pypyr.context import Context  # type: ignore
except Exception:  # pragma: no cover
    # Minimal fallback to allow type hints without dependency at runtime.
    class Context(dict):  # type: ignore
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

    def __init__(self, name: str, context: Context, is_shell: bool = False) -> None:
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
        self.context = context
        self.is_shell = is_shell

        if 'cmd' not in context:
            raise KeyError("Required key not found in context: 'cmd'")

        self._normalized: List[Mapping[str, Any]
                               ] = self._normalize_cmd(context['cmd'])

    def create_command(self, cmd_input: Mapping) -> Mapping[str, Any]:
        '''Create a pypyr.subproc.Command object from expanded step input.'''
        # This implementation normalizes to an internal dict describing the command.
        # Mapping keys:
        # - run: str
        # - save: bool
        # - cwd: Optional[Path]
        # - bytes: bool
        # - encoding: Optional[str]
        # - stdout: Optional[str | Path] (special: '/dev/null')
        # - stderr: Optional[str | Path] (special: '/dev/null', '/dev/stdout')
        # - append: bool
        run = cmd_input.get('run')
        if not run:
            raise ValueError("cmd item must have 'run'.")

        save = bool(cmd_input.get('save', False))
        cwd = cmd_input.get('cwd', None)
        cwd_path: Optional[Path] = Path(cwd) if cwd is not None else None
        out_bytes = bool(cmd_input.get('bytes', False))
        encoding = cmd_input.get('encoding', None)
        stdout = cmd_input.get('stdout', None)
        stderr = cmd_input.get('stderr', None)
        append = bool(cmd_input.get('append', False))

        base = {
            'save': save,
            'cwd': cwd_path,
            'bytes': out_bytes,
            'encoding': encoding,
            'stdout': stdout,
            'stderr': stderr,
            'append': append,
        }

        normalized: List[Mapping[str, Any]] = []
        if isinstance(run, list):
            for r in run:
                if not isinstance(r, str):
                    raise ValueError(
                        "Each 'run' item in list must be a string.")
                entry = dict(base)
                entry['run'] = r
                normalized.append(entry)
        elif isinstance(run, str):
            entry = dict(base)
            entry['run'] = run
            normalized.append(entry)
        else:
            raise ValueError("'run' must be a string or list of strings.")

        # Return the first if single, else return list. But method contract says single Command.
        # For compatibility with the rest of this class, return dict for a single command.
        if len(normalized) == 1:
            return normalized[0]
        else:
            # If caller uses create_command directly with a list run, return the first.
            return normalized[0]

    def run_step(self) -> None:
        '''Spawn a subprocess to run the command or program.
        If cmd.is_save==True, save result of each command to context 'cmdOut'.
        '''
        outputs: List[Mapping[str, Any]] = []

        for cmd in self._normalized:
            run_str: str = cmd['run']
            save: bool = bool(cmd.get('save', False))
            cwd: Optional[Path] = cmd.get('cwd')
            out_bytes: bool = bool(cmd.get('bytes', False))
            encoding: Optional[str] = cmd.get('encoding')
            stdout_tgt = cmd.get('stdout')
            stderr_tgt = cmd.get('stderr')
            append: bool = bool(cmd.get('append', False))

            # Prepare subprocess parameters
            kwargs: dict[str, Any] = {}
            kwargs['shell'] = self.is_shell
            if cwd is not None:
                kwargs['cwd'] = os.fspath(cwd)

            # Determine if stderr should redirect to stdout
            stderr_to_stdout = (isinstance(stderr_tgt, str)
                                and stderr_tgt == '/dev/stdout')

            # Handle capture when saving
            if save:
                kwargs['stdout'] = subprocess.PIPE
                kwargs['stderr'] = subprocess.STDOUT if stderr_to_stdout else subprocess.PIPE
            else:
                # stdout handling when not saving
                stdout_handle = None
                if stdout_tgt is None:
                    kwargs['stdout'] = None  # inherit
                elif isinstance(stdout_tgt, str) and stdout_tgt == '/dev/null':
                    kwargs['stdout'] = subprocess.DEVNULL
                else:
                    path = Path(stdout_tgt)
                    mode = 'ab' if append else 'wb'
                    stdout_handle = open(path, mode)
                    kwargs['stdout'] = stdout_handle

                # stderr handling when not saving
                stderr_handle = None
                if stderr_to_stdout:
                    kwargs['stderr'] = subprocess.STDOUT
                elif stderr_tgt is None:
                    kwargs['stderr'] = None  # inherit
                elif isinstance(stderr_tgt, str) and stderr_tgt == '/dev/null':
                    kwargs['stderr'] = subprocess.DEVNULL
                else:
                    path = Path(stderr_tgt)
                    mode = 'ab' if append else 'wb'
                    stderr_handle = open(path, mode)
                    kwargs['stderr'] = stderr_handle

            # Build args
            if self.is_shell:
                args: Union[str, List[str]] = run_str
            else:
                # Split into argv list
                args = shlex.split(run_str, posix=os.name != 'nt')

            # Run the subprocess
            try:
                completed = subprocess.run(args, check=False, **kwargs)
            finally:
                # Close file handles if opened for non-save
                if not save:
                    fh = kwargs.get('stdout')
                    if hasattr(fh, 'close'):
                        try:
                            fh.close()
                        except Exception:
                            pass
                    fh = kwargs.get('stderr')
                    if hasattr(fh, 'close'):
                        try:
                            fh.close()
                        except Exception:
                            pass

            # Collect and/or write outputs when saving
            if save:
                std_bytes = completed.stdout if completed.stdout is not None else b''
                err_bytes: Optional[bytes]
                if stderr_to_stdout:
                    err_bytes = None
                else:
                    err_bytes = completed.stderr if completed.stderr is not None else b''

                # If file targets specified, write the captured bytes to files.
                if stdout_tgt is not None:
                    if isinstance(stdout_tgt, str) and stdout_tgt == '/dev/null':
                        pass
                    else:
                        path = Path(stdout_tgt)
                        mode = 'ab' if append else 'wb'
                        with open(path, mode) as f:
                            f.write(std_bytes)

                if not stderr_to_stdout and (stderr_tgt is not None):
                    if isinstance(stderr_tgt, str) and stderr_tgt == '/dev/null':
                        pass
                    else:
                        path = Path(stderr_tgt)
                        mode = 'ab' if append else 'wb'
                        with open(path, mode) as f:
                            f.write(err_bytes or b'')

                # Prepare saved output
                if out_bytes:
                    out_stdout: Optional[bytes] = std_bytes if std_bytes else None
                    out_stderr: Optional[bytes] = (
                        None if stderr_to_stdout else (err_bytes if err_bytes else None))
                else:
                    sys_enc = encoding or (None)
                    if sys_enc:
                        try:
                            s_stdout = std_bytes.decode(sys_enc)
                        except Exception:
                            s_stdout = std_bytes.decode(
                                sys_enc, errors='replace')
                    else:
                        s_stdout = std_bytes.decode(errors='replace')
                    s_stdout = s_stdout.rstrip('\r\n') if s_stdout else ''
                    out_stdout = s_stdout if s_stdout else None

                    if stderr_to_stdout:
                        out_stderr = None
                    else:
                        if sys_enc:
                            try:
                                s_stderr = (err_bytes or b'').decode(sys_enc)
                            except Exception:
                                s_stderr = (err_bytes or b'').decode(
                                    sys_enc, errors='replace')
                        else:
                            s_stderr = (err_bytes or b'').decode(
                                errors='replace')
                        s_stderr = s_stderr.rstrip('\r\n') if s_stderr else ''
                        out_stderr = s_stderr if s_stderr else None

                outputs.append({
                    'returncode': completed.returncode,
                    'stdout': out_stdout,
                    'stderr': out_stderr
                })

        # Save to context if any outputs recorded
        if outputs:
            self.context['cmdOut'] = outputs[0] if len(
                outputs) == 1 else outputs

    # Internal normalization helpers

    def _normalize_cmd(self, cmd_cfg: Any) -> List[Mapping[str, Any]]:
        items: List[Mapping[str, Any]] = []

        def expand_item(item: Any) -> List[Mapping[str, Any]]:
            if isinstance(item, str):
                return [{
                    'run': item,
                    'save': False,
                    'cwd': None,
                    'bytes': False,
                    'encoding': None,
                    'stdout': None,
                    'stderr': None,
                    'append': False
                }]
            elif isinstance(item, Mapping):
                # If run is list, expand to multiple
                run_val = item.get('run')
                if isinstance(run_val, list):
                    merged: List[Mapping[str, Any]] = []
                    for r in run_val:
                        itm = dict(item)
                        itm['run'] = r
                        merged.extend(expand_item(itm))
                    return merged
                else:
                    # Create a single normalized dict
                    norm = self.create_command(item)
                    return [norm]
            else:
                raise ValueError("cmd items must be string or mapping.")

        if isinstance(cmd_cfg, str):
            items.extend(expand_item(cmd_cfg))
        elif isinstance(cmd_cfg, Mapping):
            # Top-level dict
            run_val = cmd_cfg.get('run')
            if run_val is None:
                raise ValueError("cmd dict must contain 'run'.")
            items.extend(expand_item(cmd_cfg))
        elif isinstance(cmd_cfg, list):
            for entry in cmd_cfg:
                items.extend(expand_item(entry))
        else:
            raise ValueError("cmd must be string, mapping or list.")

        return items
