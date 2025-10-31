class Data:

    def __init__(self, d):
        self.last_managed = d.get('last_managed', {}).get('time', 0)
        self.last_managed_by = d.get('last_managed', {}).get('id', '')
        self.failed_checks = d.get('failed_checks', {})
        self.iaas = d.get('iaas', {})

    def dump(self):
        return {'iaas': self.iaas, 'failed_checks': self.failed_checks}

    def __str__(self):
        return str(self.__dict__)