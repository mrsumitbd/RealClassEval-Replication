
import argparse
from typing import List


class DependenciesConfiguration:
    '''Dependency configuration class, for RuntimeContext.job_script_provider.'''

    def __init__(self, args: argparse.Namespace) -> None:
        '''Initialize.'''
        self.args = args

    def build_job_script(self, builder: 'Builder', command: List[str]) -> str:
        '''Build a job script using the provided builder and command.'''
        return builder.build(command)
