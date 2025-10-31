
import argparse
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from builder import Builder


class DependenciesConfiguration:
    '''Dependency configuration class, for RuntimeContext.job_script_provider.'''

    def __init__(self, args: argparse.Namespace) -> None:
        '''Initialize.'''
        self.args = args

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        '''Use the galaxy-tool-util library to construct a build script.'''
        from galaxy.tool_util.deps import build_script
        return build_script(builder, command)
