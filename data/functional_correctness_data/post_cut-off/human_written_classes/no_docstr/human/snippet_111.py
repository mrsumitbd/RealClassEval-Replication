from pathlib import Path
import torch
import logging
import shutil
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple, Union

class group_profile:

    def __init__(self, name: str=None, do_prof: bool=True, merge_group: bool=True, keep_merged_only: bool=True, compress: bool=True, group: Optional[torch.distributed.ProcessGroup]=None):
        self.name = name
        self.do_prof = do_prof
        self.profile = torch.profiler.profile(activities=[torch.profiler.ProfilerActivity.CPU, torch.profiler.ProfilerActivity.CUDA], record_shapes=True, with_stack=True)
        self.group = group or torch.distributed.group.WORLD
        self.merge_group = merge_group
        self.keep_merged_only = keep_merged_only
        self.compress = compress
        self.trace_file = Path('prof') / f'{self.name}' / f'rank{self.group.rank()}.json'

    def __enter__(self):
        if self.do_prof:
            self.profile.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.do_prof:
            self.profile.__exit__(exc_type, exc_val, exc_tb)
            self.trace_file.parent.mkdir(parents=True, exist_ok=True)
            logging.info(f'export chrome trace to {self.trace_file}')
            self.profile.export_chrome_trace(str(self.trace_file))
            if self.merge_group:
                self.merge_all()

    def _collect_all_to_rank0(self):
        if self.merge_group:
            torch.cuda.synchronize()
            with open(self.trace_file, 'rb') as f:
                trace_content = f.read()
            trace_content_list = [None for _ in range(self.group.size())]
            torch.distributed.gather_object(trace_content, trace_content_list if self.group.rank() == 0 else None, dst=0, group=self.group)
            torch.cuda.synchronize()
            return trace_content_list if self.group.rank() == 0 else None

    def _merge_all_trace(self, trace_content_list):
        logging.info('merge profiles...')
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            Path(tmpdir).mkdir(exist_ok=True)
            for n in range(self.group.size()):
                with open(Path(tmpdir) / f'trace_{n}.json', 'wb') as f:
                    f.write(trace_content_list[n])
            to_merge_files = [Path(tmpdir) / f'trace_{n}.json' for n in range(self.group.size())]
            merged_json = Path('prof') / f'{self.name}_merged.json'
            _merge_json(to_merge_files, merged_json, self.compress)

    def merge_all(self):
        trace_content_list = self._collect_all_to_rank0()
        if self.group.rank() == 0:
            self._merge_all_trace(trace_content_list)
        self.group.barrier()
        torch.cuda.synchronize()
        outdir = Path('prof') / f'{self.name}'
        if self.keep_merged_only:
            logging.info(f'remove profile directory: {outdir}')
            self.trace_file.unlink(missing_ok=True)
            if torch.cuda.current_device() == 0:
                shutil.rmtree(self.trace_file.parent, ignore_errors=True)