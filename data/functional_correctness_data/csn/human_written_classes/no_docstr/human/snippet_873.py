class InputsValidator:

    def __init__(self, command_validator, config_validators):
        self.command_validator = command_validator
        self.config_validators = config_validators

    def validate_command(self, job_directory, command):
        return self.command_validator.validate(job_directory, command)

    def validate_config(self, job_directory, name, path):
        config_validator = self.config_validators.get(name, None)
        valid = True
        if config_validator:
            contents = open(path, encoding='UTF-8').read()
            valid = config_validator.validate(job_directory, contents)
        return valid