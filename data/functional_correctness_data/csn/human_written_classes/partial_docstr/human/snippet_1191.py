class SystemdService:

    def __init__(self, config, service, use_instance_name):
        self.config = config
        self.service = service
        self._use_instance_name = use_instance_name
        if use_instance_name:
            prefix_instance_name = f'-{config.instance_name}'
            description_instance_name = f' {config.instance_name}'
        else:
            prefix_instance_name = ''
            description_instance_name = ''
        if self.service.count > 1:
            description_process = ' (process %i)'
        else:
            description_process = ''
        self.unit_prefix = f'galaxy{prefix_instance_name}-{service.service_name}'
        self.description = f'Galaxy{description_instance_name}{service.service_name}{description_process}'

    @property
    def unit_file_name(self):
        instance_count = self.service.count
        if instance_count > 1:
            return f'{self.unit_prefix}@.service'
        else:
            return f'{self.unit_prefix}.service'

    @property
    def unit_names(self):
        """The representation when performing commands, after instance expansion"""
        instance_count = self.service.count
        if instance_count > 1:
            unit_names = [f'{self.unit_prefix}@{i}.service' for i in range(0, instance_count)]
        else:
            unit_names = [f'{self.unit_prefix}.service']
        return unit_names