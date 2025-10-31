
class DependenciesConfiguration:
    '''Dependency configuration class, for RuntimeContext.job_script_provider.'''

    def __init__(self, args: argparse.Namespace) -> None:
        '''Initialize.'''
        self.args = args

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        '''Build job script.'''
        script = builder.build_script(command)
        return script
