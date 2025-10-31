class ArvadosKeep:
    """Files stored in Arvados Keep. Partial implementation, integration in bcbio-vm.
    """

    @classmethod
    def check_resource(self, resource):
        return resource.startswith('keep:')

    @classmethod
    def download(self, filename, input_dir, dl_dir=None):
        return None