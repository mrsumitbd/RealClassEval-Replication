from os.path import basename, dirname, exists, join

class ClientInputs:
    """Abstraction describing input datasets for a job."""

    def __init__(self, client_inputs):
        self.client_inputs = client_inputs

    def __iter__(self):
        return iter(self.client_inputs)

    @staticmethod
    def for_simple_input_paths(input_files):
        client_inputs = []
        for input_file in input_files:
            client_inputs.append(ClientInput(input_file, CLIENT_INPUT_PATH_TYPES.INPUT_PATH))
            files_path = '%s_files' % input_file[0:-len('.dat')]
            if exists(files_path):
                client_inputs.append(ClientInput(files_path, CLIENT_INPUT_PATH_TYPES.INPUT_EXTRA_FILES_PATH))
        return ClientInputs(client_inputs)