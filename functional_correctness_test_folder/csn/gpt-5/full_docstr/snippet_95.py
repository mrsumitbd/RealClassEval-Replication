from __future__ import annotations

import asyncio
import locale
import os
import shlex
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Tuple, Union


@dataclass
class SubprocessResult:
    cmd: Union[str, Sequence[str]]
    returncode: int
    stdout: Optional[Union[str, bytes]]
    stderr: Optional[Union[str, bytes]]


@dataclass
class _CommandConfig:
    run: Union[str, Sequence[str]]
    save: bool = False
    cwd: Optional[Union[str, Path]] = None
    is_bytes: bool = False
    encoding: Optional[str] = None
    stdout: Optional[Union[str, Path]] = None
    stderr: Optional[Union[str, Path]] = None
    append: bool = False


try:
    # pypyr Context is mapping-like; we only rely on mapping interface.
    from pypyr.context import Context  # type: ignore
except Exception:  # pragma: no cover
    Context = MutableMapping  # type: ignore


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
        self.context = context
        self.is_shell = bool(is_shell)

        cfg = None
        # Support both 'cmds' (preferred) and 'cmd' (fallback)
        if isinstance(context, Mapping):
            if 'cmds' in context:
                cfg = context['cmds']
            elif 'cmd' in context:
                cfg = context['cmd']
        if cfg is None:
            raise KeyError(
                'AsyncCmdStep expects "cmds" (or "cmd") in context.')

        # Build execution plan: list of units. A unit is either CommandConfig or list[CommandConfig] (serial group).
        self._units: List[Union[_CommandConfig, List[_CommandConfig]]] = []
        self._parse_config(cfg)
        self._save_any = any(c.save for c in self._iter_all_commands())

    def create_command(self, cmd_input: Mapping) -> _CommandConfig:
        '''Create pypyr.aio.subproc.Command object from expanded step input.'''
        if not isinstance(cmd_input, Mapping):
            raise TypeError('Expanded syntax must be a mapping/dict.')

        run = cmd_input.get('run')
        if run is None:
            raise KeyError('Expanded syntax requires "run".')

        save = bool(cmd_input.get('save', False))
        is_bytes = bool(cmd_input.get('bytes', False))
        encoding = cmd_input.get('encoding')
        if encoding is not None and not isinstance(encoding, str):
            raise TypeError('"encoding" must be a string or None.')
        cwd = cmd_input.get('cwd')
        stdout = cmd_input.get('stdout')
        stderr = cmd_input.get('stderr')
        append = bool(cmd_input.get('append', False))

        # The run value can be str or sequence[str]; return a base config;
        # caller will clone as needed when fan-out.
        return _CommandConfig(
            run=run,
            save=save,
            cwd=cwd,
            is_bytes=is_bytes,
            encoding=encoding,
            stdout=stdout,
            stderr=stderr,
            append=append,
        )

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
        async def runner():
            # Pre-allocate result list in start order
            total = sum(1 if isinstance(u, _CommandConfig) else len(u)
                        for u in self._units)
            results: List[Union[SubprocessResult,
                                Exception, None]] = [None] * total

            # Index mapping: for each unit, the slice where to place completed results
            slices: List[Tuple[int, int]] = []
            cursor = 0
            for u in self._units:
                if isinstance(u, _CommandConfig):
                    slices.append((cursor, cursor + 1))
                    cursor += 1
                else:
                    n = len(u)
                    slices.append((cursor, cursor + n))
                    cursor += n

            async def run_one(cfg: _CommandConfig) -> Union[SubprocessResult, Exception]:
                try:
                    return await self._run_command(cfg)
                except Exception as ex:  # capture exception as per spec
                    return ex

            async def run_serial(group: List[_CommandConfig]) -> List[Union[SubprocessResult, Exception]]:
                out: List[Union[SubprocessResult, Exception]] = []
                for cfg in group:
                    out.append(await run_one(cfg))
                return out

            tasks: List[asyncio.Task] = []
            # Map task to its slot index/slice
            # start, end, is_serial
            task_slots: List[Tuple[int, int, bool]] = []

            for idx, unit in enumerate(self._units):
                if isinstance(unit, _CommandConfig):
                    t = asyncio.create_task(run_one(unit))
                    tasks.append(t)
                    start, end = slices[idx]
                    task_slots.append((start, end, False))
                else:
                    t = asyncio.create_task(run_serial(unit))
                    tasks.append(t)
                    start, end = slices[idx]
                    task_slots.append((start, end, True))

            # Wait for all concurrently
            finished = await asyncio.gather(*tasks, return_exceptions=False)
            # Place results into their positions
            for (start, end, is_serial), value in zip(task_slots, finished):
                if not is_serial:
                    results[start] = value  # type: ignore[index]
                else:
                    seq = value  # type: ignore[assignment]
                    for i, v in enumerate(seq):
                        results[start + i] = v

            # Filter Nones (shouldn't be any)
            flat_results: List[Union[SubprocessResult, Exception]] = [
                r for r in results if r is not None]  # type: ignore[list-item]

            if self._save_any and isinstance(self.context, MutableMapping):
                self.context['cmdOut'] = flat_results

        asyncio.run(runner())

    # --------------- internals -----------------

    def _parse_config(self, cfg: Any) -> None:
        # cfg can be:
        # - str: single cmd
        # - list: items can be str, list[str], dict (expanded), or list[dict? not supported -> treat as list[str])
        # - dict (expanded) with run: str | list[str|list[str]]
        def normalize_cmd_str_or_seq(run: Union[str, Sequence[str]]) -> Union[str, Sequence[str]]:
            if isinstance(run, str):
                return run
            # ensure sequence[str]
            return list(run)

        if isinstance(cfg, str):
            self._units.append(_CommandConfig(run=cfg))
            return

        if isinstance(cfg, Mapping):
            base = self.create_command(cfg)
            run = base.run
            if isinstance(run, str):
                base.run = normalize_cmd_str_or_seq(run)
                self._units.append(base)
            else:
                # run is a list; entries can be str or list[str] (serial subgroup)
                for entry in list(run):
                    if isinstance(entry, str):
                        self._units.append(_CommandConfig(
                            run=normalize_cmd_str_or_seq(entry),
                            save=base.save,
                            cwd=base.cwd,
                            is_bytes=base.is_bytes,
                            encoding=base.encoding,
                            stdout=base.stdout,
                            stderr=base.stderr,
                            append=base.append,
                        ))
                    elif isinstance(entry, Sequence):
                        group: List[_CommandConfig] = []
                        for sub in list(entry):
                            if not isinstance(sub, str):
                                raise TypeError(
                                    'Nested "run" sub-list must contain strings.')
                            group.append(_CommandConfig(
                                run=normalize_cmd_str_or_seq(sub),
                                save=base.save,
                                cwd=base.cwd,
                                is_bytes=base.is_bytes,
                                encoding=base.encoding,
                                stdout=base.stdout,
                                stderr=base.stderr,
                                append=base.append,
                            ))
                        self._units.append(group)
                    else:
                        raise TypeError(
                            'Items in "run" list must be str or list[str].')
            return

        if isinstance(cfg, Sequence):
            for item in cfg:
                if isinstance(item, str):
                    self._units.append(_CommandConfig(run=item))
                elif isinstance(item, Mapping):
                    # expanded syntax per item
                    self._parse_config(item)
                elif isinstance(item, Sequence):
                    # serial group
                    group: List[_CommandConfig] = []
                    for sub in item:
                        if isinstance(sub, str):
                            group.append(_CommandConfig(run=sub))
                        elif isinstance(sub, Mapping):
                            # allow expanded per-subcommand inside group
                            subcfg = self.create_command(sub)
                            run = subcfg.run
                            if isinstance(run, str):
                                subcfg.run = run
                                group.append(subcfg)
                            else:
                                # If expanded sub has run list, we flatten:
                                for subrun in list(run):
                                    if not isinstance(subrun, str):
                                        raise TypeError(
                                            'Nested run list inside serial group must be strings.')
                                    group.append(_CommandConfig(
                                        run=subrun,
                                        save=subcfg.save,
                                        cwd=subcfg.cwd,
                                        is_bytes=subcfg.is_bytes,
                                        encoding=subcfg.encoding,
                                        stdout=subcfg.stdout,
                                        stderr=subcfg.stderr,
                                        append=subcfg.append,
                                    ))
                        else:
                            raise TypeError(
                                'Serial group entries must be str or mapping.')
                    self._units.append(group)
                else:
                    raise TypeError(
                        'cmds list entries must be str, list[str], or mapping.')
            return

        raise TypeError('Unsupported configuration type for cmds/cmd.')

    def _iter_all_commands(self) -> Iterable[_CommandConfig]:
        for u in self._units:
            if isinstance(u, _CommandConfig):
                yield u
            else:
                for c in u:
                    yield c

    async def _run_command(self, cfg: _CommandConfig) -> SubprocessResult:
        shell = self.is_shell
        cwd = str(cfg.cwd) if cfg.cwd is not None else None

        # stdout/stderr redirection
        stdout_spec, stdout_handle = self._map_redirect(cfg.stdout, cfg.append)
        stderr_spec, stderr_handle = self._map_redirect(
            cfg.stderr, cfg.append, allow_stdout=True)

        # choose PIPE when saving and not redirected
        want_capture = cfg.save and stdout_spec is None
        want_err_capture = cfg.save and (
            stderr_spec is None or stderr_spec == asyncio.subprocess.STDOUT)

        if want_capture:
            stdout_param = asyncio.subprocess.PIPE
        else:
            stdout_param = stdout_spec

        if want_err_capture:
            stderr_param = asyncio.subprocess.PIPE if stderr_spec is None else stderr_spec
        else:
            stderr_param = stderr_spec

        # Build command invocation
        if isinstance(cfg.run, str):
            cmd_display = cfg.run
            if shell:
                proc = await asyncio.create_subprocess_shell(
                    cfg.run,
                    stdout=stdout_param,
                    stderr=stderr_param,
                    cwd=cwd
                )
            else:
                args = shlex.split(cfg.run)
                proc = await asyncio.create_subprocess_exec(
                    *args,
                    stdout=stdout_param,
                    stderr=stderr_param,
                    cwd=cwd
                )
        else:
            # sequence args
            args_seq = list(cfg.run)
            cmd_display = args_seq
            if shell:
                # If shell=True with list, join into a string
                cmd_str = ' '.join(shlex.quote(s) for s in args_seq)
                proc = await asyncio.create_subprocess_shell(
                    cmd_str,
                    stdout=stdout_param,
                    stderr=stderr_param,
                    cwd=cwd
                )
            else:
                proc = await asyncio.create_subprocess_exec(
                    *args_seq,
                    stdout=stdout_param,
                    stderr=stderr_param,
                    cwd=cwd
                )

        out_b, err_b = await proc.communicate()

        # Close any opened file handles
        if stdout_handle is not None:
            try:
                stdout_handle.close()
            except Exception:
                pass
        if stderr_handle is not None and stderr_handle is not stdout_handle:
            try:
                stderr_handle.close()
            except Exception:
                pass

        # Prepare outputs
        if cfg.save:
            if cfg.is_bytes:
                out_v = out_b if isinstance(
                    out_b, (bytes, bytearray)) and out_b else None
                err_v = err_b if isinstance(
                    err_b, (bytes, bytearray)) and err_b else None
            else:
                enc = cfg.encoding or locale.getpreferredencoding(False)
                out_v = out_b.decode(enc).rstrip('\n') if isinstance(
                    out_b, (bytes, bytearray)) and out_b is not None else None
                err_v = err_b.decode(enc).rstrip('\n') if isinstance(
                    err_b, (bytes, bytearray)) and err_b is not None else None
        else:
            out_v = None
            err_v = None

        return SubprocessResult(
            cmd=cmd_display,
            returncode=proc.returncode,
            stdout=out_v,
            stderr=err_v
        )

    def _map_redirect(self, target: Optional[Union[str, Path]], append: bool, allow_stdout: bool = False):
        # Returns (spec, handle) for asyncio subprocess stdout/stderr param
        if target is None:
            return None, None
        t = str(target)

        if t == '/dev/null':
            return asyncio.subprocess.DEVNULL, None

        if allow_stdout and t == '/dev/stdout':
            return asyncio.subprocess.STDOUT, None

        # File path
        mode = 'ab' if append else 'wb'
        # Ensure parent dir exists
        p = Path(t)
        p.parent.mkdir(parents=True, exist_ok=True)
        f = p.open(mode)
        return f, f
