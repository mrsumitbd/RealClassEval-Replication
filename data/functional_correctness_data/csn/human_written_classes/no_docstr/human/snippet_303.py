import configobj

class ConfigProvider:

    def __init__(self):
        self.file_path = None

    def __call__(self, file_path, cmd_name):
        self.file_path = file_path
        return configobj.ConfigObj(file_path, unrepr=True)