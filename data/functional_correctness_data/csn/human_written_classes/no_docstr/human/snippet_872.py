class AllowAnyAuthorization:

    def authorize_setup(self):
        pass

    def authorize_tool_file(self, name, contents):
        pass

    def authorize_execution(self, job_directory, command_line):
        pass

    def authorize_config_file(self, job_directory, name, path):
        pass