import re

class ClientOutputs:
    """ Abstraction describing the output datasets EXPECTED by the Galaxy job
    runner client.
    """

    def __init__(self, working_directory=None, output_files=[], work_dir_outputs=None, version_file=None, dynamic_outputs=None, metadata_directory=None, job_directory=None, dynamic_file_sources=None):
        self.working_directory = working_directory
        self.metadata_directory = metadata_directory
        self.work_dir_outputs = work_dir_outputs or []
        self.output_files = output_files or []
        self.version_file = version_file
        self.dynamic_outputs = dynamic_outputs or DEFAULT_DYNAMIC_COLLECTION_PATTERN
        self.job_directory = job_directory
        self.dynamic_file_sources = dynamic_file_sources
        self.__dynamic_patterns = list(map(re.compile, self.dynamic_outputs))

    def to_dict(self):
        return dict(working_directory=self.working_directory, metadata_directory=self.metadata_directory, job_directory=self.job_directory, work_dir_outputs=self.work_dir_outputs, output_files=self.output_files, version_file=self.version_file, dynamic_outputs=self.dynamic_outputs, dynamic_file_sources=self.dynamic_file_sources)

    @staticmethod
    def from_dict(config_dict):
        return ClientOutputs(working_directory=config_dict.get('working_directory'), metadata_directory=config_dict.get('metadata_directory'), work_dir_outputs=config_dict.get('work_dir_outputs'), output_files=config_dict.get('output_files'), version_file=config_dict.get('version_file'), dynamic_outputs=config_dict.get('dynamic_outputs'), dynamic_file_sources=config_dict.get('dynamic_file_sources'), job_directory=config_dict.get('job_directory'))

    def dynamic_match(self, filename):
        return any(map(lambda pattern: pattern.match(filename), self.__dynamic_patterns))