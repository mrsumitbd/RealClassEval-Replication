import asyncio
import logging
import os
import shlex
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Mapping, Optional, Tuple, Union


@dataclass
class _CmdSpec:
    cmd: Union[str, List[str]]
    save: bool = False
    cwd: Optional[Union[str, os.PathLike]] = None
    is_bytes: bool = False
    encoding: Optional[str] = None
    stdout_path: Optional[Union[str, os.PathLike]] = None
    stderr_path: Optional[Union[str, os.PathLike]] = None
    append: bool = False


@dataclass
class _SubprocessResult:
    cmd: Union[str, List[str]]
    returncode: int
    stdout: Optional[Union[str, bytes]]
    stderr: Optional[Union[str, bytes]]


class AsyncCmdStep:
    '''A pypyr step to run executables/commands concurrently as a subprocess.
    This models a step that takes config like this in simple syntax:
        cmds:
            - <<cmd string 1>>
            - <<cmd string 2>>
    All the commands will run concurrently, in parallel.
    OR, expanded syntax is as a dict
        cmds:
            run: list[str | list[str]]. mandatory. command + args to execute.
                If list entry is another list[str], the sub-list will run in
                serial.
            save: bool. defaults False. save output to cmdOut. Treats output
                as text in the system's encoding and removes newlines at end.
            cwd: str/Pathlike. optional. Working directory for these commands.
            bytes (bool): Default False. When `save` return output bytes from
                cmds unaltered, without applying any encoding & text newline
                processing.
            encoding (str): Default None. When `save`, decode output with
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
        cmds:
          run:
            - ./my-executable --arg
            - [./another-executable --arg, ./arb-executable arghere]
          save: False
          cwd: ./path/here
    As a list in simplified syntax:
        cmds:
          - my-executable --arg
          - ./another-executable --arg
    Any or all of the list items can use expanded syntax:
        cmds:
          - ./simple-cmd-here --arg1 value
          - run: cmd here
            save: False cwd: ./path/here
          - run:
              - my-executable --arg
              - ./another-executable --arg
            save: True
            cwd: ./path/here
    Any of the list items can in turn be a list. A sub-list will run in serial.
    In this example A, B.1 & C will start concurrently. B.2 will only run once
    B.1 is finished.
        cmds:
            - A
            - [B.1, B.2]
            - C
    If save is True, will save the output to context as cmdOut.
    cmdOut will be a list of pypyr.subproc.SubprocessResult objects, in order
    executed.
    SubprocessResult has the following properties:
    cmd: the cmd/args executed
    returncode: 0
    stdout: 'stdout str here. None if empty.'
    stderr: 'stderr str here. None if empty.'
    cmdOut.returncode is the exit status of the called process. Typically 0
    means OK. A negative value -N indicates that the child was terminated by
    signal N (POSIX only).
    The run_step method does the actual work. init parses the input yaml.
    Attributes:
        logger (logger): Logger instantiated by name of calling step.
        context: (pypyr.context.Context): The current pypyr Context.
        commands (pypyr.subproc.Commands): Commands to run as subprocess.
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
        self.context = context
        self.is_shell = is_shell
        self.logger = logging.getLogger(name)

        cfg = context.get('cmds')
        if cfg is None:
            # fallback to older/alternate key
            cfg = context.get('cmd')
        if cfg is None:
            raise KeyError(
                "AsyncCmdStep requires 'cmds' (or 'cmd') in context.")

        # Parse configuration into groups of commands
        # Each element in self._groups is a list[_CmdSpec] to run in serial.
        # Groups run concurrently with each other.
        self._groups: List[List[_CmdSpec]] = self._parse_cfg(cfg)

    def create_command(self, cmd_input: Mapping) -> _CmdSpec:
        '''Create pypyr.aio.subproc.Command object from expanded step input.'''
        return self._spec_from_mapping(cmd_input)

    def run_step(self) -> None:
        '''Spawn subprocesses to run the commands asynchronously.
        If cmd.is_save==True, save aggregate result of all commands to context
        'cmdOut'.
        cmdOut will be a list of pypyr.subproc.SubprocessResult or Exception
        objects, in order executed.
        SubprocessResult has the following properties:
        cmd: the cmd/args executed
        returncode: 0
        stdout: 'stdout str here. None if empty.'
        stderr: 'stderr str here. None if empty.'
        '''
        results = asyncio.run(self._run_all_groups())
        # Flatten results preserving group order then serial order within group
        flat: List[Union[_SubprocessResult, Exception]] = []
        for grp in results:
            flat.extend(grp)
        # Save if any command had save=True
        if any(spec.save for grp in self._groups for spec in grp):
            # Transform to expected shape: keep attributes as in docstring
            self.context['cmdOut'] = flat

    # ---------------- internal helpers ----------------

    def _parse_cfg(self, cfg: Any) -> List[List[_CmdSpec]]:
        # Top-level can be:
        # - string: single command
        # - list: items of string | list (serial group) | mapping (expanded)
        # - mapping: expanded syntax with run
        if isinstance(cfg, str):
            return [[self._spec_from_mapping({'run': cfg})]]

        if isinstance(cfg, Mapping):
            return self._groups_from_expanded(cfg)

        if isinstance(cfg, Iterable):
            groups: List[List[_CmdSpec]] = []
            for item in cfg:
                if isinstance(item, str):
                    groups.append([self._spec_from_mapping({'run': item})])
                elif isinstance(item, Mapping):
                    groups.extend(self._groups_from_expanded(item))
                elif isinstance(item, Iterable):
                    # serial group: list of items, each can be str or mapping
                    serial_specs: List[_CmdSpec] = []
                    for sub in item:
                        if isinstance(sub, str):
                            serial_specs.append(
                                self._spec_from_mapping({'run': sub}))
                        elif isinstance(sub, Mapping):
                            # allow per-item expanded
                            item_groups = self._groups_from_expanded(sub)
                            # flatten: if groups_from_expanded returns multiple groups,
                            # treat them as serially concatenated here
                            for g in item_groups:
                                serial_specs.extend(g)
                        else:
                            raise TypeError(
                                f"Unsupported sub-item type in serial list: {type(sub)}")
                    if serial_specs:
                        groups.append(serial_specs)
                else:
                    raise TypeError(
                        f"Unsupported item type in cmds: {type(item)}")
            return groups

        raise TypeError(f"Unsupported cmds config type: {type(cfg)}")

    def _groups_from_expanded(self, m: Mapping) -> List[List[_CmdSpec]]:
        if 'run' not in m:
            raise KeyError("Expanded syntax requires 'run'")
        base = {k: v for k, v in m.items() if k != 'run'}
        run = m['run']
        groups: List[List[_CmdSpec]] = []
        if isinstance(run, str):
            groups.append([self._spec_from_mapping({'run': run, **base})])
        elif isinstance(run, Iterable):
            # Each element of run can be:
            # - str: a single cmd (concurrent group)
            # - list: serial group of strings or mappings
            # - mapping: a single cmd with overrides
            for elem in run:
                if isinstance(elem, str):
                    groups.append(
                        [self._spec_from_mapping({'run': elem, **base})])
                elif isinstance(elem, Mapping):
                    # this allows per-elem overrides
                    merged = dict(base)
                    merged.update(elem)
                    sub_groups = self._groups_from_expanded(merged)
                    groups.extend(sub_groups)
                elif isinstance(elem, Iterable):
                    serial_specs: List[_CmdSpec] = []
                    for sub in elem:
                        if isinstance(sub, str):
                            serial_specs.append(
                                self._spec_from_mapping({'run': sub, **base}))
                        elif isinstance(sub, Mapping):
                            merged = dict(base)
                            merged.update(sub)
                            sub_groups2 = self._groups_from_expanded(merged)
                            for g in sub_groups2:
                                serial_specs.extend(g)
                        else:
                            raise TypeError(
                                f"Unsupported sub-item type in serial list: {type(sub)}")
                    if serial_specs:
                        groups.append(serial_specs)
                else:
                    raise TypeError(
                        f"Unsupported element type in run: {type(elem)}")
        else:
            raise TypeError(f"Unsupported type for 'run': {type(run)}")
        return groups

    def _spec_from_mapping(self, m: Mapping) -> _CmdSpec:
        cmd = m.get('run')
        if cmd is None or not isinstance(cmd, (str, list)):
            raise ValueError("Command 'run' must be a string or argv list.")
        save = bool(m.get('save', False))
        cwd = m.get('cwd')
        is_bytes = bool(m.get('bytes', False))
        encoding = m.get('encoding')
        stdout_path = m.get('stdout')
        stderr_path = m.get('stderr')
        append = bool(m.get('append', False))
        return _CmdSpec(
            cmd=cmd,
            save=save,
            cwd=cwd,
            is_bytes=is_bytes,
            encoding=encoding,
            stdout_path=stdout_path,
            stderr_path=stderr_path,
            append=append,
        )

    async def _run_all_groups(self) -> List[List[Union[_SubprocessResult, Exception]]]:
        tasks = [asyncio.create_task(self._run_serial_group(group))
                 for group in self._groups]
        results = await asyncio.gather(*tasks, return_exceptions=False)
        return results

    async def _run_serial_group(self, group: List[_CmdSpec]) -> List[Union[_SubprocessResult, Exception]]:
        out: List[Union[_SubprocessResult, Exception]] = []
        for spec in group:
            try:
                res = await self._exec_one(spec)
            except Exception as ex:
                out.append(ex)
            else:
                out.append(res)
        return out

    def _open_redir(self, path: Optional[Union[str, os.PathLike]], append: bool):
        if not path:
            return None
        if isinstance(path, (str, Path)):
            s = str(path)
            if s == '/dev/null':
                return open(os.devnull, 'ab')
            # '/dev/stdout' handled separately for stderr mapping to stdout
            mode = 'ab' if append else 'wb'
            p = Path(s)
            p.parent.mkdir(parents=True, exist_ok=True)
            return open(p, mode)
        return None

    def _build_argv(self, cmd: Union[str, List[str]]) -> Tuple[Union[str, List[str]], bool]:
        if self.is_shell:
            if isinstance(cmd, list):
                # if shell=True but argv list provided, join into a string
                return ' '.join(shlex.quote(x) for x in cmd), True
            return cmd, True
        else:
            if isinstance(cmd, list):
                return cmd, False
            return shlex.split(cmd), False

    async def _exec_one(self, spec: _CmdSpec) -> _SubprocessResult:
        argv, use_shell = self._build_argv(spec.cmd)
        # stdout/err handling
        # Determine whether to capture for save
        capture_stdout = spec.save or (spec.stderr_path == '/dev/stdout')
        capture_stderr = spec.save

        stdout_file = None
        stderr_file = None
        to_stdout = asyncio.subprocess.PIPE if capture_stdout else None
        to_stderr = asyncio.subprocess.PIPE if capture_stderr else None

        # Special redirects
        if spec.stderr_path == '/dev/stdout':
            to_stderr = asyncio.subprocess.STDOUT
            capture_stderr = False  # combined in stdout

        # File outputs
        if spec.stdout_path and spec.stdout_path != '/dev/null':
            # We will tee: capture if needed, and also write to file after
            stdout_file = self._open_redir(spec.stdout_path, spec.append)
            if not capture_stdout:
                # direct write to file
                to_stdout = stdout_file

        if spec.stderr_path and spec.stderr_path not in ('/dev/null', '/dev/stdout'):
            stderr_file = self._open_redir(spec.stderr_path, spec.append)
            if not capture_stderr:
                to_stderr = stderr_file

        if spec.stdout_path == '/dev/null':
            to_stdout = asyncio.subprocess.DEVNULL
        if spec.stderr_path == '/dev/null':
            to_stderr = asyncio.subprocess.DEVNULL

        proc = await asyncio.create_subprocess_shell(
            argv if use_shell else self._argv_to_str(argv),
            stdout=to_stdout,
            stderr=to_stderr,
            cwd=str(spec.cwd) if spec.cwd else None,
        ) if use_shell else await asyncio.create_subprocess_exec(
            *argv, stdout=to_stdout, stderr=to_stderr,
            cwd=str(spec.cwd) if spec.cwd else None,
        )

        stdout_bytes, stderr_bytes = await proc.communicate()

        # If we directed to files, but also captured, tee now
        if stdout_file and stdout_bytes is not None:
            try:
                stdout_file.write(stdout_bytes)
                stdout_file.flush()
            finally:
                stdout_file.close()
        elif stdout_file:
            stdout_file.close()

        if stderr_file and stderr_bytes is not None:
            try:
                stderr_file.write(stderr_bytes)
                stderr_file.flush()
            finally:
                stderr_file.close()
        elif stderr_file:
            stderr_file.close()

        # Prepare result
        if spec.save:
            if spec.is_bytes:
                out_stdout = stdout_bytes if stdout_bytes not in (
                    None, b'') else None
                out_stderr = None
                if spec.stderr_path != '/dev/stdout':
                    out_stderr = stderr_bytes if stderr_bytes not in (
                        None, b'') else None
            else:
                enc = spec.encoding or sys.getdefaultencoding()
                out_stdout = None
                if stdout_bytes is not None:
                    out_stdout = stdout_bytes.decode(enc, errors='replace')
                    out_stdout = out_stdout.rstrip(
                        '\r\n') if out_stdout != '' else None
                out_stderr = None
                if spec.stderr_path != '/dev/stdout':
                    if stderr_bytes is not None:
                        out_stderr = stderr_bytes.decode(enc, errors='replace')
                        out_stderr = out_stderr.rstrip(
                            '\r\n') if out_stderr != '' else None
        else:
            out_stdout = None
            out_stderr = None

        return _SubprocessResult(
            cmd=spec.cmd,
            returncode=proc.returncode,
            stdout=out_stdout,
            stderr=out_stderr
        )

    def _argv_to_str(self, argv: Union[str, List[str]]) -> str:
        if isinstance(argv, str):
            return argv
        return ' '.join(shlex.quote(x) for x in argv)
