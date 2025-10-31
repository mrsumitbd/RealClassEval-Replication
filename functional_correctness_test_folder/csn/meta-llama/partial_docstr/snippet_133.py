
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
        job_script = "#!/bin/bash\n"
        job_script += "#SBATCH --job-name={}\n".format(builder.job_name)
        job_script += "#SBATCH --output={}\n".format(builder.log_file)
        job_script += "#SBATCH --error={}\n".format(builder.log_file)
        job_script += "#SBATCH --ntasks=1\n"
        job_script += "#SBATCH --cpus-per-task={}\n".format(
            builder.num_threads)
        job_script += "#SBATCH --mem={}\n".format(builder.memory)
        job_script += "#SBATCH --time={}\n".format(builder.time)
        job_script += "module load {}\n".format(' '.join(builder.modules))
        job_script += ' '.join(command) + "\n"
        return job_script
