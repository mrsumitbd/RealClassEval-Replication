import json
import os

class OrganizationWorkspace:
    MOUNT_SOURCE = os.getenv('MOUNT_SOURCE_PATH')
    MOUNT_DESTINATION = os.getenv('MOUNT_DST_PATH')
    available = False
    project_id_by_path = {}

    @classmethod
    def load(cls):
        if not (cls.MOUNT_SOURCE and cls.MOUNT_DESTINATION):
            return
        if not os.path.exists(cls.MOUNT_DESTINATION):
            return
        for name in os.listdir(cls.MOUNT_DESTINATION):
            if name in ['.QuantConnect', 'data', 'lean.json']:
                continue
            cls._process_directory(os.path.join(cls.MOUNT_DESTINATION, name))
        cls.available = True

    @classmethod
    def _process_directory(cls, path):
        config_path = os.path.join(path, 'config.json')
        if os.path.isfile(config_path):
            with open(config_path, 'r') as f:
                config_data = json.load(f)
                if 'cloud-id' in config_data:
                    cls.project_id_by_path[path] = config_data['cloud-id']
        else:
            for dir_name in os.listdir(path):
                sub_path = os.path.join(path, dir_name)
                if os.path.isdir(sub_path):
                    cls._process_directory(sub_path)