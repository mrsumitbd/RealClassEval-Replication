from hidet.runtime.compiled_module import CompiledModule, compiled_module_exists
from pathlib import Path

class CompiledProgram:

    def __init__(self, program_dir: str | Path):
        self.program_dir: Path = Path(program_dir)
        self.compiled_module = CompiledModule(str(self.program_dir / 'module'))

    def __call__(self, *args):
        return self.compiled_module(*args)