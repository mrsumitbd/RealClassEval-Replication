
class DependenciesConfiguration:
    '''Dependency configuration class, for RuntimeContext.job_script_provider.'''

    def __init__(self, args: argparse.Namespace) -> None:
        '''Initialize.'''
        self.args = args

    def build_job_script(self, builder: 'Builder', command: list[str]) -> str:
        '''Use the galaxy-tool-util library to construct a build script.'''
        from galaxy.tool_util.deps import galaxy_util_deps
        return galaxy_util_deps.build_job_script(builder, command, self.args)
